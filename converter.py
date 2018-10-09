import sys

FILE = open(sys.argv[1], 'r')
original = FILE.readline()

SCALE_FACTOR = 4.9
TERRAIN_FACTOR = 3.15
absolute_ground = 3.5

birds = []
blocks = []
pigs = []
tnts = []
platforms = []

slingshot_x = 0.0
slingshot_y = 0.0

name_bank = {
             "BLOCK_4X4_HOLLOW":"SquareHole",
             "BLOCK_4X2":"RectFat",
             "BLOCK_2X2":"SquareSmall",
             "BLOCK_1X1":"SquareTiny",
             "BLOCK_2X1":"RectTiny",
             "BLOCK_4X1":"RectSmall",
             "BLOCK_8X1":"RectMedium",
             "BLOCK_10X1":"RectBig",
             "TRIANGLE_4X4_HOLLOW":"TriangleHole",
             "TRIANGLE_4X4":"Triangle",
             "CIRCLE_4X4":"Circle",
             "CIRCLE_2X2":"CircleSmall"
             }

bird_bank = {
            "BIRD_RED":"BirdRed",
            "BIRD_BLUE":"BirdBlue",
            "BIRD_YELLOW":"BirdYellow",
            "BIRD_BLACK":"BirdBlack",
            "BIRD_WHITE":"BirdWhite"
            }


name_bank2 = {
             "SquareHole":"BLOCK_4X4_HOLLOW",
             "RectFat":"BLOCK_4X2",
             "SquareSmall":"BLOCK_2X2",
             "SquareTiny":"BLOCK_1X1",
             "RectTiny":"BLOCK_2X1",
             "RectSmall":"BLOCK_4X1",
             "RectMedium":"BLOCK_8X1",
             "RectBig":"BLOCK_10X1",
             "TriangleHole":"TRIANGLE_4X4_HOLLOW",
             "Triangle":"TRIANGLE_4X4",
             "Circle":"CIRCLE_4X4",
             "CircleSmall":"CIRCLE_2X2"
             }


bird_bank2 = {
            "BirdRed":"BIRD_RED",
            "BirdBlue":"BIRD_BLUE",
            "BirdYellow":"BIRD_YELLOW",
            "BirdBlack":"BIRD_BLACK",
            "BirdWhite":"BIRD_WHITE"
            }




if sys.argv[1][-5:] == ".json":

    # read from json file
    while(original != ""):
        original = original.strip()
        
        if original[0:17] == '"id": "Slingshot"':
            original = FILE.readline()
            original = original.strip()
            original = FILE.readline()
            original = original.strip()
            original = FILE.readline()
            original = original.strip()
            original = FILE.readline()
            original = original.strip()    
            original = FILE.readline()
            original = original.strip()
        
        if original[0:6] == '"bird_':      # find number and type of birds
            original = FILE.readline()
            original = FILE.readline()
            temp = original.split()
            name = temp[-1]
            name = name[0:-1]
            birds.append(name)
            if (slingshot_x == 0.0 and slingshot_y == 0.0):
                original = FILE.readline()
                temp = original.split()
                name = temp[-1]
                name = name[0:-1]
                slingshot_x = name
                original = FILE.readline()
                temp = original.split()
                name = temp[-1]
                name = name[0:-1]
                slingshot_y = name

        if original[0:7] == '"block_':       # find other objects
            
            original = FILE.readline()      # angle
            temp = original.split()
            angle = temp[-1]
            angle = angle[0:-1]
            angle = float(angle)
            
            original = FILE.readline()      # name / ID
            temp = original.split()
            name = temp[-1]
            name = name[0:-1]

            original = FILE.readline()      # x position
            temp = original.split()
            x = temp[-1]
            x = x[0:-1]
            x = float(x)

            original = FILE.readline()      # y position
            temp = original.split()
            y = temp[-1]
            y = y[0:]
            y = float(y)
            
            blocks.append([name,x,y,angle])
            
        original = FILE.readline()
        

    # wrtie to xml file
    f = open(sys.argv[2], "w")

    f.write('<?xml version="1.0" encoding="utf-16"?>\n')
    f.write('<Level width ="2">\n')
    f.write('<Camera x="0" y="-1" minWidth="25" maxWidth="40">\n')
    f.write('<Birds>\n')

    for bird in birds:
        f.write('<Bird type="%s"/>\n' % bird_bank[str(bird).strip('"')])
    
    f.write('</Birds>\n')
    f.write('<Slingshot x="%s" y="%s">\n' % (str((float(slingshot_x)/SCALE_FACTOR)-12.0),str(((float(slingshot_y)*-1)/SCALE_FACTOR)-absolute_ground+0.8)))
    f.write('<GameObjects>\n')

    for block in blocks:
        block[1] = (block[1]/SCALE_FACTOR)-12.0
        block[2] = ((block[2]*-1)/SCALE_FACTOR)-absolute_ground
        block[3] = (block[3] * -1)+360

    for block in blocks:
        if block[0][0:16] == '"PIG_BASIC_SMALL':
            f.write('<Pig type="BasicSmall" material="" x="%s" y="%s" rotation="%s" />\n' % (str(block[1]),str(block[2]), str(block[3])))
        elif block[0][0:4] == '"PIG':
            f.write('<Pig type="BasicMedium" material="" x="%s" y="%s" rotation="%s" />\n' % (str(block[1]),str(block[2]), str(block[3])))
        elif block[0][0:8] == '"TERRAIN':
            height = str(float(block[0].split("_")[-1].split("X")[-1][0:-1])/TERRAIN_FACTOR)
            width = str(float(block[0].split("_")[-1].split("X")[0])/TERRAIN_FACTOR)
            f.write('<Platform type="Platform" material="" x="%s" y="%s" rotation="%s" scaleX="%s" scaleY="%s" />\n' % (str(block[1]),str(block[2]), str(block[3]),width,height))
        elif block[0][0:5] == '"MISC':
            if block[0][0:19] == '"MISC_EXPLOSIVE_TNT':
                f.write('<TNT type="" x="%s" y="%s" rotation="%s" />\n' % (str(block[1]), str(block[2]), str(block[3])))
            elif block[0][0:13] == '"MISC_ESTRADE':
                height = str(float(block[0].split("_")[-1].split("X")[-1][0:-1])/TERRAIN_FACTOR)
                width = str(float(block[0].split("_")[-1].split("X")[0])/TERRAIN_FACTOR)
                f.write('<Platform type="Platform" material="" x="%s" y="%s" rotation="%s" scaleX="%s" scaleY="%s" />\n' % (str(block[1]),str(block[2]),str(block[3]),width,height))
            elif block[0][0:19] == '"MISC_RUBBER_SMILEY':
                f.write('<Block type="%s" material="stone" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank["CIRCLE_4X4"], str(block[1]), str(block[2]), str(block[3])))
            elif block[0][0:20] == '"MISC_METAL_TIRE_4X4':
                f.write('<Block type="%s" material="stone" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank["CIRCLE_4X4"], str(block[1]), str(block[2]), str(block[3])))
            elif block[0][0:20] == '"MISC_METAL_TIRE_2X2':
                f.write('<Block type="%s" material="stone" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank["CIRCLE_2X2"], str(block[1]), str(block[2]), str(block[3])))
            elif block[0][0:18] == '"MISC_METAL_PILLAR':
                f.write('<Block type="%s" material="stone" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank["BLOCK_8X1"], str(block[1]), str(block[2]), str(block[3]+90.0)))
                f.write('<Block type="%s" material="stone" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank["BLOCK_8X1"], str(block[1]-0.22), str(block[2]), str(block[3]+90.0)))
                f.write('<Block type="%s" material="stone" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank["BLOCK_8X1"], str(block[1]+0.22), str(block[2]), str(block[3]+90.0)))
            else:
                print("NEW BLOCK TYPE: %s" % block[0])
        else:
            block_name = block[0].split("_")
            material = block_name.pop(0).strip('"').lower()
            block_name = "_".join(block_name).strip('"')
            f.write('<Block type="%s" material="%s" x="%s" y="%s" rotation="%s" />\n' %
                    (name_bank[str(block_name)], material, str(block[1]), str(block[2]), str(block[3])))

    f.write('</GameObjects>\n')
    f.write('</Level>\n')
    f.close()




elif sys.argv[1][-4:] == ".xml":
    # read from xml file
    while(original != ""):
        original = original.strip()

        if original[0:5] == '<Bird':
            name = original[12:-3]
            if name != '':
                birds.append(name)
                print(birds)

        if original[0:10] == '<Slingshot':
            temp = original.split()
            name = temp[-1]
            y = name[2:-1]
            slingshot_y = y
            name = temp[-2]
            x = name[2:-1]
            slingshot_x = x

            print(slingshot_x)
            print(slingshot_y)

        if original[0:6] == '<Block':

            temp = original.split()         

            angle = temp[-2]            # angle
            angle = angle[10:-1]
            angle = float(angle)
                   
            y = temp[-3]             # y position
            y = y[3:-1]
            y = float(y)

            x = temp[-4]             # x position
            x = x[3:-1]
            x = float(x)

            material = temp[-5]
            material = material[10:-1]

            name = temp[-6]
            name = name[6:-1]
            
            blocks.append([name,x,y,angle, material])

        if original[0:4] == '<Pig':

            temp = original.split()         
            
            angle = temp[-2]            # angle
            angle = angle[10:-1]
            angle = float(angle)
                   
            y = temp[-3]             # y position
            y = y[3:-1]
            y = float(y)

            x = temp[-4]             # x position
            x = x[3:-1]
            x = float(x)

            name = temp[-5]
            name = name[6:-1]
            
            pigs.append([name,x,y,angle])

        if original[0:4] == '<TNT':

            temp = original.split()         
            
            angle = temp[-2]            # angle
            angle = angle[10:-1]
            angle = float(angle)
                   
            y = temp[-3]             # y position
            y = y[3:-1]
            y = float(y)

            x = temp[-4]             # x position
            x = x[3:-1]
            x = float(x)
  
            tnts.append([x,y,angle])

        if original[0:9] == '<Platform':

            temp = original.split()

            y = temp[-2]             # y position
            y = y[3:-1]
            y = float(y)

            x = temp[-3]             # x position
            x = x[3:-1]
            x = float(x)
            
            platforms.append([x,y,angle])

        original = FILE.readline()

    print("")
    print(blocks)
    print("")
    print(pigs)
    print("")
    print(tnts)
    print("")
    print(platforms)


    f = open(sys.argv[2], "w")

    number_birds = len(birds)

    f.write('{\n')
    f.write('"camera": [\n')
    f.write('{\n')
    f.write('"bottom": 9.684,\n')
    f.write('"id": "Slingshot",\n')
    f.write('"left": 10.08,\n')
    f.write('"right": 106.962,\n')
    f.write('"top": -44.347,\n')
    f.write('"x": 27.941,\n')
    f.write('"y": -15.862\n')
    f.write('},\n')
    f.write('{\n')
    f.write('"bottom": 9.684,\n')
    f.write('"id": "Castle",\n')
    f.write('"left": 10.08,\n')
    f.write('"right": 106.962,\n')
    f.write('"top": -44.347,\n')
    f.write('"x": 55.941,\n')
    f.write('"y": -17.332\n')
    f.write('}\n')
    f.write('],\n')
    f.write('"counts": {\n')
    f.write('"birds": %s,\n' % str(number_birds))

    number_blocks = len(blocks)+len(pigs)+len(platforms)+len(tnts)+1
    
    f.write('"blocks": %s\n' % str(number_blocks))
    f.write('},\n')
    f.write('"id": "pack4/LevelP2_103.lua",\n')
    f.write('"scoreEagle": 53000,\n')
    f.write('"scoreGold": 62000,\n')
    f.write('"scoreSilver": 55000,\n')
    f.write('"theme": "BACKGROUND_BLUE_GRASS",\n')

    f.write('"world": {\n')

    for i in range(number_birds):
        f.write('"bird_%s": {\n' % str(i+1))
        f.write('"angle": 0,\n')
        f.write('"id": "%s",\n' % str(bird_bank2[birds[i]]))
        f.write('"x": %s,\n' % str(6 - (i*3)))
        f.write('"y": 0.0\n')
        f.write('},\n')
            
    block_number = 1
    for block in blocks:
        block[1] = (block[1]+12.0)*SCALE_FACTOR
        block[2] = ((block[2]+absolute_ground)*SCALE_FACTOR)
        block[3] = ((block[3]-360) * -1)

    for platform in platforms:
        platform[0] = (platform[0]+12.0)*SCALE_FACTOR
        platform[1] = ((platform[1]+absolute_ground)*SCALE_FACTOR)
        platform[2] = ((platform[2]-360) * -1)

    for pig in pigs:
        pig[1] = (pig[1]+12.0)*SCALE_FACTOR
        pig[2] = ((pig[2]+absolute_ground)*SCALE_FACTOR)

        
    for tnt in tnts:
        tnt[0] = (tnt[0]+12.0)*SCALE_FACTOR
        tnt[1] = ((tnt[1]+absolute_ground)*SCALE_FACTOR)
        tnt[2] = ((tnt[2]-360) * -1)

    for i in blocks:
        rotation = i[3]
        f.write('"block_%s": {\n' % str(block_number))
        f.write('"angle": %s,\n' % str(rotation))
        material = str(i[4])
        print(material)
        if material == "wood":
            f.write('"id": "WOOD_')
        if material == "ice":
            f.write('"id": "ICE_')
        if material == "stone":
            f.write('"id": "STONE_')
        f.write('%s",\n' % str(name_bank2[i[0]]))
        f.write('"x": %s,\n' % str(i[1]))
        f.write('"y": %s\n' % str(i[2]*-1))
        f.write('},\n')

        block_number = block_number + 1

    for platform in platforms:
        f.write('"block_%s": {\n' % str(block_number))
        f.write('"angle": %s,\n' % str(platform[2]))
        f.write('"id": "TERRAIN_TEXTURED_HILLS_5X2",\n')
        f.write('"x": %s,\n' % str(platform[0]))
        f.write('"y": %s\n' % str(platform[1]*-1))
        f.write('},\n')
        block_number = block_number + 1

    f.write('"block_%s": {\n' % str(block_number))
    f.write('"angle": %s,\n' % 360.0)
    f.write('"id": "TERRAIN_TEXTURED_HILLS_32X2",\n')
    f.write('"x": %s,\n' % -10.0)
    f.write('"y": %s\n' % 1.0)
    f.write('},\n')
    block_number = block_number + 1

    for tnt in tnts:
        f.write('"block_%s": {\n' % str(block_number))
        f.write('"angle": %s,\n' % str(tnt[2]))
        f.write('"id": "MISC_EXPLOSIVE_TNT",\n')
        f.write('"x": %s,\n' % str(tnt[0]))
        f.write('"y": %s\n' % str(tnt[1]*-1))
        f.write('},\n')
        block_number = block_number + 1

    for j in pigs:
        f.write('"block_%s": {\n' % str(block_number))
        f.write('"angle": 0.0,\n')
        f.write('"id": "PIG_BASIC_SMALL",\n')
        f.write('"x": %s,\n' % str(j[1]))
        f.write('"y": %s\n' % str(j[2]*-1))

        if j != pigs[-1]:
            f.write('},\n')
        else:
            f.write('}\n')

        block_number = block_number + 1

    for t in tnts:
        continue
         
    f.write('}\n')
    f.write('}\n')

    f.close()


