#Version History 

# 20-08-2018 Created

# Decorator function with getter and setter to return
# properties. Getter raises error - so constants cannot be changed
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class Constants(object):
    @constant
    def DATA_READY():
        return 5
    @constant
    def EXT_RECIEVE():
        return 7
    @constant
    def SEND_NOW():
        return 11
    @constant
    def DATA_RX_ACK_1():
        return 19
    @constant
    def DATA_RX_ACK_2():
        return 21        
    @constant
    def DATA_RX():
        return 23
    @constant
    def SHUTDOWN_DEMAND():
        return 29
    @constant
    def POWER_CHECK():
        return 8    
    @constant
    def SYSTEM_ACTIVE():
        return 10
    @constant
    def PANIC():
        return 12
    @constant
    def DATA_TX_ACK_1():
        return 16
    @constant
    def DATA_TX_ACK_2():
        return 18
    @constant
    def DATA_TX():
        return 22
    @constant
    def UART_DISABLE_CHECK():
        return 8
            


