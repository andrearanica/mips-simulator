from libs.Datapath import Datapath

if __name__ == "__main__":
    datapath = Datapath()
    instructions = [
        '00100001000010000000000000000001'
    ]
    datapath.run(instructions)