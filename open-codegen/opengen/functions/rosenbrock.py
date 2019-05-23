from casadi import *


def rosenbrock(u_, p_):
    if not isinstance(p_, SX) or p_.size()[0] != 2:
        raise Exception('illegal parameter p_ (must be SX of size (2,1))')
    if not isinstance(u_, SX):
        raise Exception('illegal parameter u_ (must be SX)')
    nu = u_.size()[0]
    a = p_[0]
    b = p_[1]
    ros_fun = 0
    for i in range(nu-1):
        ros_fun += b*(u_[i+1]-u_[i]**2)**2 + (a-u_[i])**2
    return ros_fun
