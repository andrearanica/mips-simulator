from libs.Datapath import Datapath

if __name__ == '__main__':
    datapath = Datapath()
    instructions = [
        '00100001000010000000000000000001',
        '00000001000010000100100000100000'
    ]
    datapath.run(instructions)