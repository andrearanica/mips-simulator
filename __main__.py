from libs.Simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator()
    file_path = input('Insert file path: ')
    simulator.file_path = file_path
    simulator.run()
