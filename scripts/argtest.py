import argparse

def main(mask):
    print(mask)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses the ANTs ImageMath executable to calulate the total brightness of an image')
    parser.add_argument('-m','--mask',
                        help="name of the image to use as a mask")
    args=parser.parse_args()
    main(args.mask)    
