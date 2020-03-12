class Room(object):

    def __init__(self, roomName, roomCapacity,isLab,isPhysicsLab,id):
        self.id = id
        self.room = roomName
        self.capacity = roomCapacity
        self.isLab = isLab
        self.isPhysicsLab = isPhysicsLab
