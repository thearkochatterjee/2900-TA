path = "D:/air motor/air motor backup/air_motor_rpm.ino"
original = open(path, "r")
o_code = original.readlines()
original.close()
replacement = open("D:/air motor/air_motor_rpm/air_motor_rpm.ino","w")
replacement.writelines(o_code)
replacement.close()
print("done")