import sys
import epp_utils as epp

def main(argv):
    sum = 0.0
    for val in [l.strip() for l in sys.stdin.readlines()]:
        try:
            number = float(val)
            sum += number
        except ValueError as detail:
            epp.err("Error on value " + val + " " + str(detail))
    epp.write("Somme = %f" % sum)
if __name__ == "__main__":
    main(sys.argv[1:])