import gym
import rospy
import roslaunch
import numpy as np
import os
import math

from gym import utils, spaces
from gym_gazebo.envs import gazebo_env
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

from sensor_msgs.msg import LaserScan
from gazebo_msgs.msg import ModelStates

from gym.utils import seeding
from scipy.spatial.transform import Rotation

class GazeboCafeTurtlebotLidarEnv(gazebo_env.GazeboEnv):

    def __init__(self):
        # Launch the simulation with the given launchfile name
        gazebo_env.GazeboEnv.__init__(self, "GazeboCafeTurtlebotLidar_v0.launch")
        self.vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=5)
        self.robot_pos_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.RobotPosCallback, queue_size=5)
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)

        self.action_space = spaces.Discrete(3) #F,L,R
        self.goal = {"x": float(os.environ['GOAL_X']), "y": float(os.environ['GOAL_Y'])}
        self.last_action = 0

        self._seed()

    def RobotPosCallback(self, msg):
        self.robot_pos = msg.pose[-1].position
        self.robot_rot = msg.pose[-1].orientation

    def discretize_observation(self,data,new_ranges):
        discretized_ranges = []
        min_range = 0.2
        done = False
        # mod = len(data.ranges)/new_ranges
        for i, item in enumerate(data.ranges):
            if i != 0 and i != 19:
                if data.ranges[i] == float ('Inf'):
                    discretized_ranges.append(10)
                elif np.isnan(data.ranges[i]):
                    discretized_ranges.append(0)
                else:
                    discretized_ranges.append(data.ranges[i])
            if (min_range > data.ranges[i] > 0):
                #these sensor points are always below the minimum range
                if i != 0 and i != 19:
                    done = True
                    print("min range: " + str(min_range) + " > data.ranges[i] " + str(data.ranges[i]) + " range number [i]: " + str(i))
        return discretized_ranges,done

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):

        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/unpause_physics service call failed")

        if action == 0: #FORWARD
            vel_cmd = Twist()
            vel_cmd.linear.x = 1.0 # 0.6
            vel_cmd.angular.z = 0.0
            self.vel_pub.publish(vel_cmd)
        elif action == 1: #LEFT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.2
            vel_cmd.angular.z = 1.0
            self.vel_pub.publish(vel_cmd)
        elif action == 2: #RIGHT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.2
            vel_cmd.angular.z = -1.0
            self.vel_pub.publish(vel_cmd)

        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass
        
        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/pause_physics service call failed")

        state,done = self.discretize_observation(data,20)
        
        # reward setting
        reward = 0
        # termination
        ## collision with obstacles
        if done:
            reward = -200
            return state, reward, done, {}
        
        ## arrive goal
        if math.hypot(self.goal["x"]-self.robot_pos.x, self.goal["y"]-self.robot_pos.y) < 0.2:
            reward = 500
            done = True
            return state, reward, done, {}
        
        # while moving
        ## Fast
        rot = Rotation.from_quat(np.array([self.robot_rot.x, self.robot_rot.y, self.robot_rot.z, self.robot_rot.w]))
        robot_yaw = rot.as_euler('ZXY')[0]
        
        if action == 0:
            vel_angle = robot_yaw
            v = 1.0
        elif action == 1:
            vel_angle = robot_yaw + 1.0 * 0.1 # 10Hz
            v = 0.2
        elif action == 2:
            vel_angle = robot_yaw - 1.0 * 0.1
            v = 0.2
        pos_to_goal_vec_angle = math.atan2(self.goal["y"]-self.robot_pos.y, self.goal["x"]-self.robot_pos.x)
        v_goal = v * math.cos(pos_to_goal_vec_angle-vel_angle)
        fast_reward = v_goal*5
        
        # print("Fast: ", fast_reward)
        reward = reward + fast_reward
        
        ## Safe
        d_min = min(state)
        safe_reward = d_min
        reward = reward + safe_reward
        # print("Safe: ", safe_reward)
        
        ## Prevent spilling coffee
        coffee_reward = 0
        if (action == 1 and self.last_action == 2) or (action == 2 and self.last_action == 1):
            coffee_reward = - 1
        reward = reward + coffee_reward
        # print("Coffee: ", coffee_reward)
        # print("reward: ", reward)
        
        self.last_action = action

        return state, reward, done, {}

    def reset(self):

        # Resets the state of the environment and returns an initial observation.
        rospy.wait_for_service('/gazebo/reset_simulation')
        try:
            #reset_proxy.call()
            self.reset_proxy()
        except (rospy.ServiceException) as e:
            print ("/gazebo/reset_simulation service call failed")

        # Unpause simulation to make observation
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            #resp_pause = pause.call()
            self.unpause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/unpause_physics service call failed")

        #read laser data
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/pause_physics service call failed")

        state = self.discretize_observation(data,5)

        return state
