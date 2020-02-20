import requests
import re
import string
from bs4 import BeautifulSoup
import csv
import time
import sys
import os


File_Location = 'C:\\Users\\vanbrec\\Documents\\Software Architecture\\MHWData\\'


def scrape_weapon(URL, Weapons_list):
    
    page = requests.get(URL)

    soup = BeautifulSoup(page.content,'html.parser')

    #Selecting the armor html table
    table = soup.find('table')
    weapon_stats = table.find('tbody')
    #Making each row of the table it's own object
    rows = weapon_stats.find_all('tr')
    z=0
    #Iterate through each row and extract the needed data (Armor Name, Rarity, Skills, Defense, Slots, Elemental Defenses)
    print("Scraping: ", end='')
    for row in rows:
        print("/-\|"[z % 4], end="\b")
        z += 1

        Weapon_Info = []
        columns = row.find_all('td')
        #print(columns)
        #weapon name
        #names = columns.find('a')
        weapon_name = columns[0].find('a').text.replace('\n', '').replace('" ','"')
        Weapon_Info.append(weapon_name)

        rarity = columns[0].find('small').text.replace('Rarity ', '')
        Weapon_Info.append(rarity)
        
        TrueAttack = row.find('rt').text
        Attack = row.find("ruby").text.replace(TrueAttack, '')
        Weapon_Info.append(Attack)
        Weapon_Info.append(TrueAttack)

        statcheck = columns[2].find('small')
        ElementType = "None"
        ElementStat = "0"
        ElementType2 = "None"
        ElementStat2 = "0"
        AffStat = "0"
        DefStat = "0"
        SealLvl = "None"
        #Weapon Stats
        if ("div" in str(statcheck)):
            stats = statcheck.find_all('div')
            
            #
            #UNIQUE CODE FOR DUAL BLADES MULTIPLE ELEMENTS
            #
            
            if ('type=2' in str(URL)):
                i = 0
                for stat in stats:
                    if ("element" in str(stat)):
                        #Dual Blade First Element
                        if (i == 0):
                            ElementStat = stat.text.replace('\n', '').replace(' ','')
                            if ("1.png" in str(stat)):
                                ElementType = "Fire"
                            if ("2.png" in str(stat)):
                                ElementType = "Water"
                            if ("3.png" in str(stat)):
                                ElementType = "Ice"
                            if ("4.png" in str(stat)):
                                ElementType = "Thunder"
                            if ("5.png" in str(stat)):
                                ElementType = "Dragon"
                            if ("6.png" in str(stat)):
                                ElementType = "Poison"
                            if ("7.png" in str(stat)):
                                ElementType = "Paralysis"
                            if ("8.png" in str(stat)):
                                ElementType = "Sleep"
                            if ("9.png" in str(stat)):
                                ElementType = "Blast"
                            if ('(' in ElementStat):
                                ElementStat = ElementStat.replace('(', '').replace(')', '')
                                ElementType = "Hidden " + ElementType
                            i = i+1
                        #Dual Blade Second Element
                        elif (i == 1):
                            ElementStat2 = stat.text.replace('\n', '').replace(' ','')
                            if ("1.png" in str(stat)):
                                ElementType2 = "Fire"
                            if ("2.png" in str(stat)):
                                ElementType2 = "Water"
                            if ("3.png" in str(stat)):
                                ElementType2 = "Ice"
                            if ("4.png" in str(stat)):
                                ElementType2 = "Thunder"
                            if ("5.png" in str(stat)):
                                ElementType2 = "Dragon"
                            if ("6.png" in str(stat)):
                                ElementType2 = "Poison"
                            if ("7.png" in str(stat)):
                                ElementType2 = "Paralysis"
                            if ("8.png" in str(stat)):
                                ElementType2 = "Sleep"
                            if ("9.png" in str(stat)):
                                ElementType2 = "Blast"
                            if ('(' in ElementStat):
                                ElementStat2 = ElementStat2.replace('(', '').replace(')', '')
                                ElementType2 = "Hidden " + ElementType2
                    elif ("affinity.png" in str(stat)):
                        AffStat = stat.text.replace('\n', '').replace(' ','').replace('%', '').replace('+', '')
                    elif ("defense.png" in str(stat)):
                        DefStat = stat.text.replace('\n', '').replace(' ','')
                    elif ("elderseal.png" in str(stat)):
                        SealLvl = stat.text.replace('\n', '').replace(' ','')
                #Fix incorect stats on dual element blades
                if (str(statcheck).count('element') == 2):
                    ElementStat = int(ElementStat)*10
                    ElementStat2 = int(ElementStat2)*10
                Weapon_Info.append(ElementType)
                Weapon_Info.append(ElementStat)
                Weapon_Info.append(ElementType2)
                Weapon_Info.append(ElementStat2)
                Weapon_Info.append(AffStat)
                Weapon_Info.append(DefStat)
                Weapon_Info.append(SealLvl)
            
            #
            #END OF DUAL BLADES SECTION
            #

            #Element, Affinity, Defense, & Elder Seal
            else:
                for stat in stats:
                    if ("element" in str(stat)):
                        ElementStat = stat.text.replace('\n', '').replace(' ','')
                        if ("1.png" in str(stat)):
                            ElementType = "Fire"
                        if ("2.png" in str(stat)):
                            ElementType = "Water"
                        if ("3.png" in str(stat)):
                            ElementType = "Ice"
                        if ("4.png" in str(stat)):
                            ElementType = "Thunder"
                        if ("5.png" in str(stat)):
                            ElementType = "Dragon"
                        if ("6.png" in str(stat)):
                            ElementType = "Poison"
                        if ("7.png" in str(stat)):
                            ElementType = "Paralysis"
                        if ("8.png" in str(stat)):
                            ElementType = "Sleep"
                        if ("9.png" in str(stat)):
                            ElementType = "Blast"
                        if ('(' in ElementStat):
                            ElementStat = ElementStat.replace('(', '').replace(')', '')
                            ElementType = "Hidden " + ElementType
                    elif ("affinity.png" in str(stat)):
                        AffStat = stat.text.replace('\n', '').replace(' ','').replace('%', '').replace('+', '')
                    elif ("defense.png" in str(stat)):
                        DefStat = stat.text.replace('\n', '').replace(' ','')
                    elif ("elderseal.png" in str(stat)):
                        SealLvl = stat.text.replace('\n', '').replace(' ','')
                Weapon_Info.append(ElementType)
                Weapon_Info.append(ElementStat)
                Weapon_Info.append(AffStat)
                Weapon_Info.append(DefStat)
                Weapon_Info.append(SealLvl)
        #Append Element, Affinity, Defense, & Elder Seal
        else:
            #Dual Blades Append
            if ('type=2' in str(URL)):
                Weapon_Info.append(ElementType)
                Weapon_Info.append(ElementStat)
                Weapon_Info.append(ElementType2)
                Weapon_Info.append(ElementStat2)
                Weapon_Info.append(AffStat)
                Weapon_Info.append(DefStat)
                Weapon_Info.append(SealLvl)
            #Weapon Append
            else:
                Weapon_Info.append(ElementType)
                Weapon_Info.append(ElementStat)
                Weapon_Info.append(AffStat)
                Weapon_Info.append(DefStat)
                Weapon_Info.append(SealLvl)

        #Sharpness Data
        SharpnessR = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-red")['style']))) * 4))
        SharpnessO = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-orange")['style']))) * 4))
        SharpnessY = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-yellow")['style']))) * 4))
        SharpnessG = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-green")['style']))) * 4))
        SharpnessB = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-blue")['style']))) * 4))
        SharpnessW = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-white")['style']))) * 4))
        SharpnessP = str(int(float("".join(re.findall("\d+\.\d+|\d+", row.find('div', class_="sharpness-purple")['style']))) * 4))
        MaxSharpness = str(int(SharpnessR) + int(SharpnessO) + int(SharpnessY) + int(SharpnessG) + int(SharpnessB) + int(SharpnessW) + int(SharpnessP))

        #Weapon Skill
        if ('<a href' in str(columns[3])):
            Skill = columns[3].find('a').text
        else:
            Skill = "None"
        
        #Gems
        if ('img' in str(columns[4])):
            slotCounts = columns[4].find_all('img')
            slot=''
            #Gem Slots
            if(len(slotCounts) >= 1):
                for i in range(len(slotCounts)):
                    slots=''
                    #Gem Size 1
                    if ("slot_size_1.png" in str(slotCounts[i])):
                        slot = slot + "Slot " + str(i+1) + " -- Level 1 Gem Slot     "
                        slots = '1'
                        Weapon_Info.append(slots)
                    #Gem Size 2
                    if ("slot_size_2.png" in str(slotCounts[i])):
                        slot = slot + "Slot " + str(i+1) + " -- Level 2 Gem Slot     "
                        slots = '2'
                        Weapon_Info.append(slots)
                    #Gem Size 3
                    if ("slot_size_3.png" in str(slotCounts[i])):
                        slot = slot + "Slot " + str(i+1) + " -- Level 3 Gem Slot     "
                        slots = '3'
                        Weapon_Info.append(slots)
                    #Gem Size 4
                    if ("slot_size_4.png" in str(slotCounts[i])):
                        slot = slot + "Slot " + str(i+1) + " -- Level 4 Gem Slot     "
                        slots = '4'
                        Weapon_Info.append(slots)
                if (len(slotCounts) == 1):
                    slots = 'None'
                    Weapon_Info.append(slots)
                    Weapon_Info.append(slots)
                if (len(slotCounts) == 2):
                    slots = 'None'
                    Weapon_Info.append(slots)
        else:
            slot = "No Slots"
            slots = "None"
            Weapon_Info.append(slots)
            Weapon_Info.append(slots)
            Weapon_Info.append(slots)

        
        #
        #HUNTING HORN NOTES AND MELODIES
        #
        if ('type=5' in str(URL)):
            Melody_URL = 'https://mhworld.kiranico.com/melodies'
            Melody_page = requests.get(Melody_URL)
            Melody_soup = BeautifulSoup(Melody_page.content,'html.parser')
            Melody_table = Melody_soup.find_all('table')
            Melody_rows = Melody_table[0].find_all('tr')
            Melodies = []
            for Melody_row in Melody_rows:
                Melody_columns = Melody_row.find_all('td')
                #Self improvement has two different boosts, finds which boost a horn can play 
                if ('Self-improvement' in str(Melody_columns)):
                    Melody_types = Melody_columns[2].find_all('div')
                    i = 0
                    #Melodies
                    for Melody_type in Melody_types:
                        Melody = []
                        Melody_options = []
                        Melody_name = Melody_type.text
                        Melody.append(Melody_name)
                        Melody_notes = Melody_columns[1].find_all('div')[i]
                        #Notes For Melody
                        for Melody_note in Melody_notes:
                            if ('note-0' in str(Melody_note)):
                                Melody_options.append('purple')
                            if ('note-1' in str(Melody_note)):
                                Melody_options.append('red')
                            if ('note-2' in str(Melody_note)):
                                Melody_options.append('orange')
                            if ('note-3' in str(Melody_note)):
                                Melody_options.append('yellow')
                            if ('note-4' in str(Melody_note)):
                                Melody_options.append('green')
                            if ('note-5' in str(Melody_note)):
                                Melody_options.append('blue')
                            if ('note-6' in str(Melody_note)):
                                Melody_options.append('cyan')
                            if ('note-7' in str(Melody_note)):
                                Melody_options.append('white')
                        Melody_options = sorted(list(set(Melody_options)))
                        Melody.append(Melody_options)
                        i = i+1
                        Melodies.append(Melody)
                #Gathers all Melody Data
                else:
                    i = 0
                    Melody = []
                    Melody_name = Melody_columns[0].find('div').text
                    Melody.append(Melody_name)
                    Melody_notes = Melody_columns[1].find_all('div')
                    for Melody_note in Melody_notes:
                        Melody_options = []
                        Melody_order = Melody_note.find_all('span')
                        #Notes for Melodies
                        for order in Melody_order:
                            if ('note-0' in str(order)):
                                Melody_options.append('purple')
                            if ('note-1' in str(order)):
                                Melody_options.append('red')
                            if ('note-2' in str(order)):
                                Melody_options.append('orange')
                            if ('note-3' in str(order)):
                                Melody_options.append('yellow')
                            if ('note-4' in str(order)):
                                Melody_options.append('green')
                            if ('note-5' in str(order)):
                                Melody_options.append('blue')
                            if ('note-6' in str(order)):
                                Melody_options.append('cyan')
                            if ('note-7' in str(order)):
                                Melody_options.append('white')
                        Melody_options = sorted(list(set(Melody_options)))
                        Melody.append(Melody_options)
                    Melodies.append(Melody)

            Notes = []
            find_notes = columns[3].find_all('span')
            for note in find_notes:
                if ('note-0' in str(note)):
                    Notes.append('purple')
                if ('note-1' in str(note)):
                    Notes.append('red')
                if ('note-2' in str(note)):
                    Notes.append('orange')
                if ('note-3' in str(note)):
                    Notes.append('yellow')
                if ('note-4' in str(note)):
                    Notes.append('green')
                if ('note-5' in str(note)):
                    Notes.append('blue')
                if ('note-6' in str(note)):
                    Notes.append('cyan')
                if ('note-7' in str(note)):
                    Notes.append('white')
            Weapon_Info.append(Notes)
            Usable_Melodies = []
            #All Melodies
            for a in range(len(Melodies)):
                #One Melody
                for b in range(len(list(Melodies[a]))):
                    Note_check = 0
                    #One Note set in Melody
                    if b == 0:
                        continue
                    for c in range(len(list(Melodies[a][b]))):
                        if Melodies[a][b][c] in list(sorted(Notes)):
                            Note_check = Note_check + 1
                    if Note_check == len(list(Melodies[a][b])):
                        Usable_Melodies.append(Melodies[a][0])
            Usable_Melodies = list(set(Usable_Melodies))
            Weapon_Info.append(Usable_Melodies)


        #
        #END OF HUNTING HORN SECTION
        #

        
        if ('shelling.png' in str(columns[3])):
            GL_Shelling = columns[3].find('small').text.replace('\n', '').replace(Skill,'').replace(' ', '').replace('Lv', ' Lv ')
            Weapon_Info.append(GL_Shelling)
        if ('type=8' in str(URL)):
            SA_Phial = columns[3].find('small').text.replace('\n', '').replace(Skill,'').replace(' ', '').replace('Phial', ' Phial ').replace('Element', ' Element')
            Weapon_Info.append(SA_Phial)
        if ('type=9' in str(URL)):
            CB_Phial = columns[3].find('small').text.replace('\n', '').replace(Skill,'').replace(' ', '').replace('Phial', ' Phial ').replace('Element', ' Element')
            Weapon_Info.append(CB_Phial)
        if ('type=10' in str(URL)):
            KinB = columns[3].find('small').text.replace('\n', '').replace(Skill,'').replace(' ', '').replace('Boost', ' Boost'). replace('&', ' & ').replace('Upgrade', ' Upgrade')
            Weapon_Info.append(KinB)
        Weapon_Info.append(Skill)


        #print("Name: " + weapon_name + " | Rarity " + rarity + " | Attack: " + Attack + " | Small Attack: " + TrueAttack + " | Element: " + 
        #ElementType + " " + str(ElementStat) + "  Affinity " + AffStat + "  Defense " + DefStat + "  Elderseal " + SealLvl + " | Skill: " +
        #Skill + "\n" + slot + "\nSharpness: Red-" + SharpnessR + " Hits / Orange-" + SharpnessO + " Hits / Yellow-" + SharpnessY +
        #" Hits / Green-" + SharpnessG + " Hits / Blue-" + SharpnessB + " Hits / White-" + SharpnessW + " Hits / Purple-" + SharpnessP +
        #" Hits | Max Sharpness: " + MaxSharpness + " Hits\n")
        
        Weapon_Info.append(MaxSharpness)
        Weapon_Info.append(SharpnessR)
        Weapon_Info.append(SharpnessO)
        Weapon_Info.append(SharpnessY)
        Weapon_Info.append(SharpnessG)
        Weapon_Info.append(SharpnessB)
        Weapon_Info.append(SharpnessW)
        Weapon_Info.append(SharpnessP)
        Weapons_list.append(Weapon_Info)
        sys.stdout.flush()
        #time.sleep(0.005)
    return Weapons_list

    #for weapon_stat in table:
    #    print(weapon_stat)
    #    sys.stdout.flush()
    #    sleep(5)
    



def make_files(File_Location):
    Weapons_list = []
    scrape_weapon(URLGreat_Sword, Weapons_list)
    with open(File_Location + 'MHWData_GreatSword.csv', 'w', newline='') as csvfile:
        GSColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(GSColumns)
        csvwriter.writerows(Weapons_list)
    print("Great Sword -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLSword_Shield, Weapons_list)
    with open(File_Location + 'MHWData_SwordShield.csv', 'w', newline='') as csvfile:
        SSColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(SSColumns)
        csvwriter.writerows(Weapons_list)
    print("Sword and Shield -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLDual_Blades, Weapons_list)
    with open(File_Location + 'MHWData_DualBlades.csv', 'w', newline='') as csvfile:
        DBColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element(1)', 'Element Stat(1)', 'Element(2)', 'Element Stat(2)', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(DBColumns)
        csvwriter.writerows(Weapons_list)
    print("Dual Blade -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLLong_Sword, Weapons_list)
    with open(File_Location + 'MHWData_LongSword.csv', 'w', newline='') as csvfile:
        LSColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(LSColumns)
        csvwriter.writerows(Weapons_list)
    print("Long Sword -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLHammer, Weapons_list)
    with open(File_Location + 'MHWData_Hammer.csv', 'w', newline='') as csvfile:
        HColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(HColumns)
        csvwriter.writerows(Weapons_list)
    print("Hammer -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLHunting_Horn, Weapons_list)
    with open(File_Location + 'MHWData_HuntingHorn.csv', 'w', newline='') as csvfile:
        HHColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Notes', 'Melodies', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(HHColumns)
        csvwriter.writerows(Weapons_list)
    print("Hunting Horn -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLLance, Weapons_list)
    with open(File_Location + 'MHWData_Lance.csv', 'w', newline='') as csvfile:
        LColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(LColumns)
        csvwriter.writerows(Weapons_list)
    print("Lance -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLGun_Lance, Weapons_list)
    with open(File_Location + 'MHWData_GunLance.csv', 'w', newline='') as csvfile:
        GLColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Shelling', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(GLColumns)
        csvwriter.writerows(Weapons_list)
    print("Gun Lance -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLSwitch_Axe, Weapons_list)
    with open(File_Location + 'MHWData_SwitchAxe.csv', 'w', newline='') as csvfile:
        SAColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Phial Type', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(SAColumns)
        csvwriter.writerows(Weapons_list)
    print("Switch Axe -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLCharge_Blade, Weapons_list)
    with open(File_Location + 'MHWData_ChargeBlade.csv', 'w', newline='') as csvfile:
        CBColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Phial Type', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(CBColumns)
        csvwriter.writerows(Weapons_list)
    print("Charge Blade -------- Complete!")
    Weapons_list = []
    scrape_weapon(URLInsect_Glaive, Weapons_list)
    with open(File_Location + 'MHWData_InsectGlaive.csv', 'w', newline='') as csvfile:
        IGColumns=['Name', 'Rarity', 'Attack', 'True Attack', 'Element', 'Element Stat', 'Affinity(%)', 'Defense', 'Elderseal', 'Gem Slot 1(Lvl)',
        'Gem Slot 2(Lvl)', 'Gem Slot 3(Lvl)', 'Kinsect Bonus', 'Skill', 'Max Sharpness', 'Red Sharpness', 'Orange Sharpness', 'Yellow Sharpness', 'Green Sharpness',
        'Blue Sharpness', 'White Sharpness', 'Purple Sharpness']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(IGColumns)
        csvwriter.writerows(Weapons_list)
    print("Insect Glaive -------- Complete!")



    print("All Scraping Complete!")

#Run
URLGreat_Sword = 'https://mhworld.kiranico.com/weapons?type=0'
URLSword_Shield = 'https://mhworld.kiranico.com/weapons?type=1'
URLDual_Blades = 'https://mhworld.kiranico.com/weapons?type=2'
URLLong_Sword = 'https://mhworld.kiranico.com/weapons?type=3'
URLHammer = 'https://mhworld.kiranico.com/weapons?type=4'
URLHunting_Horn = 'https://mhworld.kiranico.com/weapons?type=5'
URLLance = 'https://mhworld.kiranico.com/weapons?type=6'
URLGun_Lance = 'https://mhworld.kiranico.com/weapons?type=7'
URLSwitch_Axe = 'https://mhworld.kiranico.com/weapons?type=8'
URLCharge_Blade = 'https://mhworld.kiranico.com/weapons?type=9'
URLInsect_Glaive = 'https://mhworld.kiranico.com/weapons?type=10'

try:
    make_files(File_Location)

except FileNotFoundError:
    print('\rLocation not found, files will be located on user desktop\nChange File Location in code if a different file location is desired')
    File_Location = 'C:\\Users\\' + os.getlogin() + '\\Desktop\\'
    make_files(File_Location)