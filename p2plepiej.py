import btpeer


def main():
	print('Enter msg: ')
	x = input()
	p1 = btpeer.BTPeer(4, x)
	# p1.mainloop()
	print('Enter msg: ')
	x = input()
	p1.connectandsend()
	print("done")
	print('Enter msg: ')
	x = input()
	print(p1.getpeerids())

if __name__ == '__main__':
    main()
