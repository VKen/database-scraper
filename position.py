# keyword match:

# check function
def checkdev(listofdev,startoftag=3,option=0):
    global notag
    notag = []
    check = 0
    for x in listofdev:
        count = 0
        for y in x[startoftag:]: # check for empty
            if not y:
                count += 1
        if count == len(x[startoftag:]):
            check += 1
            notag.append(x[:startoftag])
            if option == 1:
                x.insert(startoftag,'NoTag')
        else:
            if option == 1:
                x.insert(startoftag,'Tag')
    return check

def posappend(setlisting):
# Thanks
    for x in setlisting:
        if 'thank' in x[1] or 'Thank' in x[1] or 'THank' in x[1] or 'THANK' in x[1] or 'thanx' in x[1] or 'Thanx' in x[1] or 'THX' in x[1]:
            x.append('Thanks')
        else:
            x.append('')
    
    # Testers
    for x in setlisting:
        if 'ontest' in x[1] or 'ittest' in x[1] or 'reatest' in x[1] or 'rotestor' in x[1]: # contest, fittest, greatest, protestor
            x.append('')
        elif 'Test' in x[1] or 'test' in x[1] or 'TEST' in x[1]:
            x.append('Tester')
        else:
            x.append('')

    #Designers
    for x in setlisting:
        if 'Design' in x[1] or 'design' in x[1] or 'DESIGN' in x[1] or 'DesigN' in x[1]:
            x.append('Designer')
        else:
            x.append('')
    
    #Quality Assurance
    for x in setlisting:
        if 'QA' in x[1] or 'Quality' in x[1] or 'QUALITY' in x[1] or 'quality' in x[1] or 'Assurance' in x[1] or 'assurance' in x[1] or 'ASSURANCE' in x[1]:
            x.append('QA')
        else:
            x.append('')
    
    #Programming
    
    for x in setlisting:
        if 'Programing' in x[1] or 'programing' in x[1] or 'Programm' in x[1] or 'programm' in x[1] or 'Coding' in x[1] or 'Code' in x[1]:
            x.append('Programmer')
            x.append('')
        if 'Program' in x[1] or 'program' in x[1] or 'PROGRAM' in x[1]:
            x.append('')
            x.append('Program')
        else:
            x.append('')
            x.append('')
    
    #Director
    for x in setlisting:
        if 'Director' in x[1] or 'director' in x[1] or 'direction' in x[1] or 'Direction' in x[1] or 'directed' in x[1] or 'Directed' in x[1]:
            x.append('Director')
        else:
            x.append('')
    
    #Artist
    for x in setlisting:
        if 'Art' in x[1] or 'artis' in x[1] or 'Dart' in x[1] or 'dart' in x[1] in x[1] or 'Graphic' in x[1] or 'GRAPHIC' in x[1] or 'graphic' in x[1] or 'Illustr' in x[1] or 'illustr' in x[1] or 'ILLUSTR' in x[1]:
            x.append('Artist')
        else:
            x.append('')
    
    #Manager
    
    for x in setlisting:
        if 'manage' in x[1] or 'Manage' in x[1] or 'MANAGE' in x[1]: 
            x.append('Management')
        else:
            x.append('')
    #Lead
    
    for x in setlisting:
        if 'lead' in x[1] or 'Lead' in x[1] or 'LEAD' in x[1]: 
            x.append('Lead')
        else:
            x.append('')
    
    #Voice
    
    for x in setlisting:
        if 'Voice' in x[1] or 'voice' in x[1] or 'VOICE' in x[1]: 
            x.append('Voice')
        else:
            x.append('')
    
    #Producer
    
    for x in setlisting:
        if 'Produce' in x[1] or 'produce' in x[1] or 'PRODUCE' in x[1] or 'PRduce' in x[1]: 
            x.append('Producer')
        else:
            x.append('')
    
    #Production and product
    
    for x in setlisting:
        if 'Production' in x[1] or 'production' in x[1] or 'PRODUCTION' in x[1]:
            x.append('Production')
            x.append('')
        elif 'Product' in x[1] or 'product' in x[1] or 'PRODUCT' in x[1]:
            x.append('')
            x.append('Product')
        else:
            x.append('')
            x.append('')
    
    
    #Audio, sound, music, recording, song
    
    for x in setlisting:
        if 'Audio' in x[1] or 'audio' in x[1] or 'AUDIO' in x[1]:
            x.append('Audio')
        else:
            x.append('')

   
    for x in setlisting:
        if 'Sound' in x[1] or 'sound' in x[1] or 'SOUND' in x[1] or 'SFX' in x[1]:
            x.append('Sound')
        else:
            x.append('')

    for x in setlisting:
        if 'Music' in x[1] or 'music' in x[1] or 'MUSIC' in x[1]:
            x.append('Music')
        else:
            x.append('')

    for x in setlisting:
        if 'Recording' in x[1] or 'recording' in x[1] or 'RECORDING' in x[1]: 
            x.append('Recording')
        else:
            x.append('')

    for x in setlisting:
        if 'Song' in x[1] or 'song' in x[1] or 'SONG' in x[1]: 
            x.append('Song')
        else:
            x.append('')

    #Marketing
    
    for x in setlisting:
        if 'Market' in x[1] or 'market' in x[1] or 'MARKET' in x[1]:
            x.append('Marketing')
        else:
            x.append('')
    
    #Developement
    for x in setlisting:
        if 'Develop' in x[1] or 'develop' in x[1] or 'DEVELOP' in x[1]:
            x.append('Development')
        else:
            x.append('')
    
    #Animation
    
    for x in setlisting:
        if 'Animat' in x[1] or 'animat' in x[1] or 'ANIMAT' in x[1]:
            x.append('Animation')
        else:
            x.append('')
    
    # Localization
    
    for x in setlisting:
        if 'Locali' in x[1] or 'locali' in x[1] or 'LOCALI' in x[1]:
            x.append('Localization')
        else:
            x.append('')
    
    # Technical
    for x in setlisting:
        if 'Tech' in x[1] or 'techi' in x[1] or 'TECH' in x[1]:
            x.append('Technical')
        else:
            x.append('')
    
    # Assistant
    
    for x in setlisting:
        if 'Assist' in x[1] or 'assist' in x[1] or 'ASSIST' in x[1]:
            x.append('Assistant')
        else:
            x.append('')
    
    # Creative
    
    for x in setlisting:
        if 'Creative' in x[1] or 'creative' in x[1] or 'CREATIVE' in x[1]:
            x.append('Creative')
        else:
            x.append('')
    
    # Effect
    
    for x in setlisting:
        if 'Effect' in x[1] or 'effect' in x[1] or 'EFFECT' in x[1]:
            x.append('Effects')
        else:
            x.append('')
    
    # Engineering and Engine
    
    for x in setlisting:
        if 'Engineer' in x[1] or 'engineer' in x[1] or 'ENGINEER' in x[1]:
            x.append('Engineering')
            x.append('')
        elif 'Engine' in x[1] or 'engine' in x[1] or 'ENGINE' in x[1]:
            x.append('')
            x.append('Engine')
        else:
            x.append('')
            x.append('')
    
    # Coordinator
    
    for x in setlisting:
        if 'Coordinat' in x[1] or 'coordinat' in x[1] or 'COORDINAT' in x[1] or 'Cordinat' in x[1] or 'cordinat' in x[1] or 'CORDINAT' in x[1]:
            x.append('Coordinator')
        else:
            x.append('')
    
    # Analyst
    
    for x in setlisting:
        if 'Analy' in x[1] or 'analy' in x[1] or 'ANALY' in x[1]:
            x.append('Analyst')
        else:
            x.append('')
    
    # Associate
    
    for x in setlisting:
        if 'Assoc' in x[1] or 'assoc' in x[1] or 'ASSOC' in x[1]:
            x.append('Associate')
        else:
            x.append('')
    
    # Supervisor
    
    for x in setlisting:
        if 'Supervis' in x[1] or 'supervis' in x[1] or 'SUPERVIS' in x[1]:
            x.append('Supervisor')
        else:
            x.append('')
    
    # Sales
    
    for x in setlisting:
        if 'Sales' in x[1] or 'sales' in x[1] or 'SALES' in x[1]:
            x.append('Sales')
        else:
            x.append('')
    
    # Software
    
    for x in setlisting:
        if 'Software' in x[1] or 'software' in x[1] or 'SOFTWARE' in x[1]:
            x.append('Software')
        else:
            x.append('')
    
    
    # President and VP
    
    for x in setlisting:
        if 'Vice-P' in x[1] or 'Vice P' in x[1] or 'ViceP' in x[1] or 'VICE P' in x[1] or 'VP' in x[1]:
            x.append('')
            x.append('Vice President')
        elif 'President' in x[1] or 'president' in x[1] or 'PRESIDENT' in x[1]:
            x.append('President')
            x.append('')
        else:
            x.append('')
            x.append('')

    # CEO
    for x in setlisting:
        if 'faceoff' in x[1] or 'oiceove' in x[1]:
            x.append('')
        elif 'CEO' in x[1] or 'Ceo' in x[1] or 'ceo' in x[1]:
            x.append('CEO')
        else:
            x.append('')

    # senior
    
    for x in setlisting:
        if 'Senior' in x[1] or 'senior' in x[1] or 'SENIOR' in x[1]:
            x.append('Senior')
        else:
            x.append('')
    
    # Operations
    
    for x in setlisting:
        if 'Operation' in x[1] or 'operation' in x[1] or 'OPERATION' in x[1]:
            x.append('Operations')
        else:
            x.append('')
    
    # Modeling
    
    for x in setlisting:
        if 'Model' in x[1] or 'model' in x[1] or 'MODEL' in x[1]:
            x.append('Modeling')
        else:
            x.append('')
    
    # Publishing

    for x in setlisting:
        if 'Publish' in x[1] or 'publish' in x[1] or 'PUBLISH' in x[1]:
            x.append('Publisher')
        else:
            x.append('')

    # Legal
    
    for x in setlisting:
        if 'Legal' in x[1] or 'legal' in x[1] or 'LEGAL' in x[1]:
            x.append('Legal')
        else:
            x.append('')

    # Translate
    
    for x in setlisting:
        if 'Translat' in x[1] or 'translat' in x[1] or 'TRANSLAT' in x[1]:
            x.append('Translation')
        else:
            x.append('')

    # History and Story

    for x in setlisting:
        if 'histor' in x[1] or 'Histor' in x[1] or 'HISTOR' in x[1]:
            x.append('History')
            x.append('')
        elif 'Story' in x[1] or 'story' in x[1] or 'STORY' in x[1]:
            x.append('')
            x.append('Story')
        else:
            x.append('')
            x.append('')


    # Writer
    
    for x in setlisting:
        if 'Writ' in x[1] or 'writ' in x[1] or 'WRIT' in x[1]:
            x.append('Writer')
        else:
            x.append('')

    # Editor

    for x in setlisting:
        if 'Editor' in x[1] or 'editor' in x[1] or 'EDITOR' in x[1]:
            x.append('Editor')
        else:
            x.append('')

    # Editing

    for x in setlisting:
        if 'Editing' in x[1] or 'editing' in x[1] or 'EDITING' in x[1]:
            x.append('Editing')
        else:
            x.append('')

    # Executive
    
    for x in setlisting:
        if 'Executiv' in x[1] or 'executiv' in x[1] or 'EXECUTIV' in x[1]:
            x.append('Executive')
        else:
            x.append('')

    # Manual and Documentation

    for x in setlisting:
        if 'Manua' in x[1] or 'MAnua' in x[1] or 'manua' in x[1] or 'MANUA' in x[1] or 'Manue' in x[1]:
            x.append('Manual')
        else:
            x.append('')

    for x in setlisting:
        if 'Docum' in x[1] or 'docum' in x[1] or 'DOCUM' in x[1]:
            x.append('Documentation')
        else:
            x.append('')

    # Actor

    for x in setlisting:
        if 'ractor' in x[1] or 'tactor' in x[1] or 'Factor' in x[1] or 'FACTOR' in x[1] or 'factor' in x[1] or 'reactor' in x[1] or 'dactor' in x[1] or 'nactor' in x[1]:
            x.append('')
        elif 'actor' in x[1] or 'Actor' in x[1] or 'ACTOR' in x[1]:
            x.append('Actor')
        else:
            x.append('')

    # Public Relations

    for x in setlisting:
        if 'PRE' in x[1] or 'PRO' in x[1]:
            x.append('')
        elif 'PR' in x[1] or 'Public Re' in x[1] or 'public Re' in x[1] or 'PUBLIC RE' in x[1] or 'public re' in x[1]:
            x.append('PR')
        else:
            x.append('')

    # Cast and casting

    for x in setlisting:
        if 'CASTLE' in x[1] or 'castle' in x[1] or 'Castle' in x[1] or 'dcast' in x[1] or 'DCAST' in x[1] or 'dCast' in x[1]:
            x.append('')
            x.append('')
        elif 'Casting' in x[1] or 'casting' in x[1] or 'CASTING' in x[1]:
            x.append('Casting')
            x.append('')
        elif 'Cast' in x[1] or 'CAST' in x[1] or ' cast' in x[1]:
            x.append('')
            x.append('Cast')
        else:
            x.append('')
            x.append('')

    # Support
    for x in setlisting:
        if 'Support' in x[1] or 'support' in x[1] or 'SUPPORT' in x[1]:
            x.append('Support')
        else:
            x.append('')

    # Talent
    for x in setlisting:
        if 'Talent' in x[1] or 'talent' in x[1] or 'TALENT' in x[1]:
            x.append('Talent')
        else:
            x.append('')

    # Concept
    for x in setlisting:
        if 'Concept' in x[1] or 'concept' in x[1] or 'CONCEPT' in x[1]:
            x.append('Concept')
        else:
            x.append('')

    # Motion Capture
    for x in setlisting:
        if 'Motion Cap' in x[1] or 'Motion cap' in x[1] or 'motion cap' in x[1] or 'MOTION CAP' in x[1] or 'MotionCap' in x[1] or 'motioncap' in x[1] or 'MOTIONCAP' in x[1] or 'Motions Cap' in x[1] or 'Motions cap' in x[1]:
            x.append('Motion Capture')
        else:
            x.append('')

    # Adminstrative
    for x in setlisting:
        if 'Administra' in x[1] or 'administra' in x[1] or 'ADMINISTRA' in x[1]:
            x.append('Adminstrative')
        else:
            x.append('')

    # Staff
    for x in setlisting:
        if 'Staff' in x[1] or 'STAFF' in x[1] or 'staff' in x[1]:
            x.append('staff')
        else:
            x.append('')

    # Research
    for x in setlisting:
        if 'Research' in x[1] or 'research' in x[1] or 'RESEARCH' in x[1]:
            x.append('Research')
        else:
            x.append('')

    # Composer
    for x in setlisting:
        if 'Compose' in x[1] or 'compose' in x[1] or 'COMPOSE' in x[1]:
            x.append('Composer')
        else:
            x.append('')

    # Planning
    for x in setlisting:
        if 'Plann' in x[1] or 'plann' in x[1] or 'PLANN' in x[1]:
            x.append('Planning')
        else:
            x.append('')

    # Packaging
    for x in setlisting:
        if 'Packag' in x[1] or 'packag' in x[1] or 'PACKAG' in x[1]:
            x.append('Packaging')
        else:
            x.append('')

    # Publicity
    for x in setlisting:
        if 'Publici' in x[1] or 'publici' in x[1]:
            x.append('Publicity')
        else:
            x.append('')

    # Lighting
    for x in setlisting:
        if 'Lighting' in x[1] or 'lighting' in x[1] or 'LIGHTING' in x[1]:
            x.append('Lighting')
        else:
            x.append('')

    # Created
    for x in setlisting:
        if 'Created' in x[1] or 'created' in x[1]:
            x.append('Created')
        else:
            x.append('')

    # Cinematic
    for x in setlisting:
        if 'Cinemat' in x[1] or 'cinemat' in x[1] or 'CINEMAT' in x[1]:
            x.append('Cinematic')
        else:
            x.append('')

    # Vocalist
    for x in setlisting:
        if 'Vocalis' in x[1] or 'vocalist' in x[1]:
            x.append('Vocalist')
        else:
            x.append('')

    # Finance
    for x in setlisting:
        if 'Financ' in x[1] or 'financ' in x[1] or 'FINANC' in x[1]:
            x.append('Finance')
        else:
            x.append('')

    # License
    for x in setlisting:
        if 'Licens' in x[1] or 'licens' in x[1] or 'LICENS' in x[1]:
            x.append('License')
        else:
            x.append('')
    
    # Promotion
    for x in setlisting:
        if 'Promo' in x[1] or 'promo' in x[1] or 'PROMO' in x[1]:
            x.append('Promotion')
        else:
            x.append('')

    # Script and Scripting:
    for x in setlisting:
        if 'anscrip' in x[1] or 'escript' in x[1] or 'ANSCRIP' in x[1] or 'ESCRIPT' in x[1]:
            x.append('')
            x.append('')
        elif 'Scriptin' in x[1] or 'scriptin' in x[1] or 'SCRIPTIN' in x[1]:
            x.append('Scripting')
            x.append('')
        elif 'Script' in x[1] or 'script' in x[1] or 'SCRIPT' in x[1]:
            x.append('')
            x.append('Script')
        else:
            x.append('')
            x.append('')

    # Debug
    for x in setlisting:
         if 'debug' in x[1] or 'Debug' in x[1] or 'DEBUG' in x[1]:
            x.append('Debug')
         else:
            x.append('')

    # Web
    for x in setlisting:
        if 'Web' in x[1] or 'web' in x[1] or'WEB' in x[1]:
            x.append('Web')
        else:
            x.append('')
    # Core
    for x in setlisting:
        if 'Core' in x[1] or 'CORE' in x[1] or ' core' in x[1]:
            x.append('Core')
        else:
            x.append('')

    # Project
    for x in setlisting:
        if 'Project' in x[1] or 'project' in x[1] or 'PROJECT' in x[1]:
            x.append('Project')
        else:
            x.append('')

    # Level
    for x in setlisting:
        if 'Level' in x[1] or 'level' in x[1] or 'LEVEL' in x[1]:
            x.append('Level')
        else:
            x.append('')

    # Character
    for x in setlisting:
        if 'Character' in x[1] or 'character' in x[1] or 'CHARACTER' in x[1]:
            x.append('Character')
        else:
            x.append('')

    # Service
    for x in setlisting:
        if 'Service' in x[1] or 'service' in x[1] or 'SERVICE' in x[1]:
            x.append('Service')
        else:
            x.append('')

    # Brand
    for x in setlisting:
        if 'Branden' in x[1] or 'Brando' in x[1] or 'Brandy' in x[1] or 'embrand' in x[1] or 'ibrand' in x[1]:
            x.append('')
        elif 'Brand' in x[1] or 'brand' in x[1] or 'BRAND' in x[1]:
            x.append('Brand')
        else:
            x.append('')

    # Video
    for x in setlisting:
        if 'Video' in x[1] or 'video' in x[1] or 'VIDEO' in x[1]:
            x.append('Video')
        else:
            x.append('')

    # Business
    for x in setlisting:
        if 'Business' in x[1] or 'business' in x[1] or 'BUSINESS' in x[1]:
            x.append('Business')
        else:
            x.append('')

    # Human Resource
    for x in setlisting:
        if 'Human Resource' in x[1] or 'human resouce' in x[1] or 'HUMAN RESOURCE' in x[1]:
            x.append('Human Resource')

    # Author
    for x in setlisting:
        if 'thoriz' in x[1] or 'thorit' in x[1] or 'THORIZ' in x[1] or 'THORIT' in x[1]:
            x.append('')
        elif 'Author' in x[1] or 'author' in x[1] or 'AUTHOR' in x[1]:
            x.append('Author')
        else:
            x.append('')

    # Screenplay
    for x in setlisting:
        if 'creenplay' in x[1]:
            x.append('Screenplay')
        else:
            x.append('')

    # Screenwriter
    for x in setlisting:
        if 'creenwri' in x[1]:
            x.append('Screenwriter')
        else:
            x.append('')

    # Acknowledgement
    for x in setlisting:
        if 'cknowle' in x[1]:
            x.append('Acknowledgement')
        else:
            x.append('')

    # Photo
    for x in setlisting:
        if 'Photo' in x[1] or 'photo' in x[1] or 'PHOTO' in x[1]:
            x.append('Photo')
        else:
            x.append('')

    # Studio
    for x in setlisting:
        if 'Studio' in x[1] or 'studio' in x[1] or 'STUDIO' in x[1]:
            x.append('Studio')
        else:
            x.append('')

    # Texture
    for x in setlisting:
        if 'Textur' in x[1] or 'textur' in x[1] or 'TEXTUR' in x[1]:
            x.append('Texture')
        else:
            x.append('')

    # Speech
    for x in setlisting:
        if 'Speech' in x[1] or 'speech' in x[1] or 'SPEECH' in x[1]:
            x.append('Speech')
        else:
            x.append('')

######
# tag listing
######

def taglist(strlist,startoftag=3):
    global taglisting
    taglisting = []
    listlen = len(strlist[0][startoftag:])
    for y in range(listlen):
        for x in strlist:
            if x[y+3]:
                taglisting.append([x[y+startoftag]])
                break
    for tags in taglisting:
        for x in strlist:
            if tags[0] in x:
                ind = taglisting.index(tags)
                taglisting[ind].append(x[1])
        print (str(tags[0]))
            
            
    
