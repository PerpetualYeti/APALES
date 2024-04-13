from gcodeParameter import gCodeParameteriser

def main():
    print("Hello from driver")
    parameteriser = gCodeParameteriser('Wood_Parameters.txt', 'Handala.nc')
    parameteriser.read_parameter()
    parameteriser.update_parameter()


if __name__ == "__main__":
    main()