from copy import copy

from numpy.random import rand, randn
from numpy import array, cos, sin, arctan2, pi
from numpy.linalg import norm


class Explorer(object):
    def __init__(self,x=0., y=0., dist_mu=0.2, dist_sigma=0.1):
        """Initialize Explorer class

        :param float dist_mu, dist_sigma: mean and standard deviation for sampling the distance of the next target
        """
        self.origin = array([x,y])
        self.dist_mu = dist_mu
        self.dist_sigma = dist_sigma
        self.current_pos = array([0., 0.])
        self.previous_angle = 0.0
        #self.previous_pos = array([0.,0.])

    def sample(self, neg_feedback=False,prop = 1.0):
        """ Returns a new target x, y. The returned coordinate is also stored in self.current_pos.
            The previous coordinate is saved in self.previous_pos

            :param bool neg_feedback: indicate if there is a negative feedback due to the previous position or not. Default: False
            :param float prop: scales the distance in case the feedback is provided by
        """

        tmp_current = copy(self.current_pos)
        if neg_feedback:
            #angle = 0
            #angle = arctan2(self.origin[0] - tmp_current[0],self.origin[1] - tmp_current[1])* 180 / pi
            angle = arctan2(self.origin[1] - tmp_current[1],self.origin[0] - tmp_current[0])
            #print angle
            if prop != 0:
                dist = max(prop,1) *  norm(self.origin - tmp_current)
            else:
                dist = norm(self.origin - tmp_current)
            #self.current_pos = tmp_current - self.previous_pos
        else:
            angle = 2*pi * rand()
            dist = self.dist_mu + self.dist_sigma * randn()
        self.current_pos += dist * array([cos(angle), sin(angle)])
        self.previous_pos = tmp_current
        self.previous_angle = angle
        return self.current_pos
