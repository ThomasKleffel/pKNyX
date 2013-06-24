
import time

from pknyx.api import Device, Stack, ETS


class MOB(ETS):

    _gadName = {1: {'name': "heating",
                    1: {'name': "setpoint",
                        1: "living",
                        2: "bedroom 1",
                        3: "bedroom 2",
                        4: "bedroom 3"
                        },
                    2: {'name': "temperature",
                        1: "living",
                        2: "bedroom 1",
                        3: "bedroom 2",
                        4: "bedroom 3"
                        }
                    },
                2: {'name': "lights",
                    1: {'name': None,
                        1: 'living',
                       },
                    2: {'name': "etage",
                        1: None,
                        2: "bedroom 1"
                       }
                    }
                }


class Dev(Device):

    # Datapoints (= Group Objects) definition
    DP_01 = dict(name="dp_1", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)
    DP_02 = dict(name="dp_2", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)
    DP_03 = dict(name="dp_3", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)
    DP_04 = dict(name="dp_4", dptId="1.001", flags="CWTU", priority="low", defaultValue=0.)

    DESC = "Truc bidule"


stack = Stack()   # Borg
mob = MOB(stack)  # Borg

dev1 = Dev(name="dev1", desc="Device 1", address="1.1.1")
dev2 = Dev(name="dev2", desc="Device 2", address="1.1.2")

mob.register(dev1)
mob.register(dev2)

mob.link(dev=dev1, dp="dp_1", gad=("1/1/1", "2/1/1"))
mob.link(dev=dev1, dp="dp_2", gad="1/1/2")
mob.link(dev=dev1, dp="dp_3", gad="1/1/3")
mob.link(dev=dev1, dp="dp_4", gad="1/1/4")

mob.link(dev=dev2, dp="dp_1", gad="1/2/1")
mob.link(dev=dev2, dp="dp_2", gad=("1/2/2", "2/2/2"))
mob.link(dev=dev2, dp="dp_3", gad="1/1/3")
#mob.link(dev=dev2, dp="dp_4", gad="1/1/4")

mob.printMapTable(by="gad")
print
print
mob.printMapTable(by="dp")

stack.start()
time.sleep(60)
