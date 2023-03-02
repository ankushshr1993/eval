import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import logging
from middleware.settings import KL_FILTER_P

# Get an instance of a logger
logger = logging.getLogger(__name__)


class KLFilter(object):
    # raw data
    # dim_x is number of states variable
    f = KalmanFilter(dim_x=2, dim_z=1)

    def __init__(self):
        self.f.x = np.array([2., 0.])
        self.f.F = np.array([[1., 1.], [0., 1.]])
        self.f.H = np.array([[1., 0.]])
        self.f.P *= KL_FILTER_P if KL_FILTER_P else 1000.
        self.f.R = 1
        self.f.Q = Q_discrete_white_noise(dim=2, dt=0.01, var=0.13)
        # print("Filter P: {}, R: {}".format(self.f.P, self.f.R))

    def run_filter(self, new_data):
        z = new_data  # new data
        self.f.predict()

        pref_x = np.copy(self.f.x)

        self.f.update(z)
        # logger.info("\n\n-----------------------------")
        # logger.info("Pred data: %s State: %s " % (pref_x, self.f.x))
        # logger.info("Q Matrix: %s" % self.f.Q)
        # logger.info("-----------------------------\n\n")
        return pref_x
        # return self.f.x
