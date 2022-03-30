lv = int(input(":"))


for l in range(lv):
    for s in range(lv - l):
        print("",end=" ")
    for star in range(l+1):
        print("* ", end="")
    print()


"""
   *
  * *
 * * *
* * * *
"""