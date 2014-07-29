# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

TRAILERS_HD = {
       101: 'AEYXe8MXuZo',  # Leon: The Professional
       534: 'W6GWhOvSAf4',  # Terminator Salvation
       550: 'ZwaBbL6fmgs',  # Fight Club
      1495: 'Kfq9U2tWWGo',  # Kingdom of Heaven
     13475: 'iGAHnZ555nI',  # Star Trek
     19995: '5PSNL1qE6VY',  # Avatar
     20504: 'kAMUv22y1og',  # The Book of Eli
     49049: 'qv-6dNqqnMA',  # Dredd
     49051: 'SDnYMbYB-nU',  # The Hobbit: An Unexpected Journey
     54138: 'sJNyGFqgyag',  # Star Trek Into Darkness
     57158: 'OPVWy1tFXuc',  # The Hobbit: The Desolation of Smaug
     59967: '2iQuhsmtfHw',  # Looper
     62177: 'TEHWDA_6e3M',  # Brave
     70981: 'GfiJ-E0S4YY',  # Prometheus
     76203: 'KrDg_6rxCzs',  # 12 Years A Slave
     86838: 'GPAlUz1hUkA',  # Seven Psychopaths
    106646: 'iszwuX1AK6A',  # The Wolf of Wall Street
    109443: 'NzNUkWFDuKQ',  # Anchorman 2
    109445: 'TbQm5doF_Uc',  # Frozen
    168672: 'h5Cb4SFt7gE',  # American Hustle
}


TOP_250 = [
    # 1
    ("The Shawshank Redemption", 1994),                                 
    # 2
    ("The Godfather", 1972),
    #
    ("The Godfather: Part II", 1974),
    #
    ("The Dark Knight", 2008),
    #
    ("Pulp Fiction", 1994),
    #
    ("Il buono, il brutto, il cattivo", 1966),
    #
    ("Schindler's List", 1993),
    #
    ("12 Angry Men", 1957),
    #
    ("The Lord of the Rings: The Return of the King", 2003),
    #
    ("Fight Club", 1999),
    #
    ("The Lord of the Rings: The Fellowship of the Ring", 2001),
    #
    ("Star Wars: Episode V - The Empire Strikes Back", 1980),
    #
    ("Inception", 2010),
    #
    ("Forrest Gump", 1994),
    #
    ("One Flew Over the Cuckoo's Nest", 1975),
    #
    ("The Lord of the Rings: The Two Towers", 2002),
    #
    ("Goodfellas", 1990),
    #
    ("Star Wars", 1977),
    #
    ("The Matrix", 1999),
    #
    ("Shichinin no samurai", 1954),
    #
    ("Cidade de Deus", 2002),
    #
    ("Se7en", 1995),
    #
    ("The Usual Suspects", 1994),
    #
    ("The Silence of the Lambs", 2000),
    #
    ("C'era una volta il West", 1968),
    #
    ("It's a Wonderful Life", 1946),
    #
    ("Léon", 1994),
    #
    ("Casablanca", 1942),
    #
    ("La vita è bella", 1997),
    #
    ("Raiders of the Lost Ark", 1981),
    #
    ("Psycho", 1960),
    #
    ("American History X", 1998),
    #
    ("Rear Window", 1954),
    #
    ("City Lights", 1931),
    #
    ("Saving Private Ryan", 1998),
    #
    ("Sen to Chihiro no kamikakushi", 2001),
    #
    ("Intouchables", 2011),
    #
    ("Memento", 2000),
    #
    ("Modern Times", 1936),
    #
    ("Terminator 2: Judgment Day", 1991),
    #
    ("Sunset Blvd.", 1950),
    #
    ("The Pianist", 2002),
    #
    ("Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb", 1964),
    #
    ("Apocalypse Now", 1979),
    #
    ("The Green Mile", 1999),
    #
    ("The Departed", 2006),
    #
    ("Gladiator", 2000),
    #
    ("Back to the Future", 1985),
    #
    ("Alien", 1979),
    #
    ("The Dark Knight Rises", 2012),
    #
    ("Django Unchained", 2012),
    #
    ("The Prestige", 2006),
    #
    ("Das Leben der Anderen", 2006),
    #
    ("The Great Dictator", 1940),
    #
    ("The Shining", 1980),
    #
    ("Nuovo Cinema Paradiso", 1988),
    #
    ("The Lion King", 1994),
    #
    ("Paths of Glory", 1957),
    #
    ("American Beauty", 1999),
    #
    ("WALL·E", 2008),
    #
    ("North by Northwest", 1959),
    #
    ("Le fabuleux destin d'Amélie Poulain", 2001),
    #
    ("Citizen Kane", 1941),
    #
    ("Aliens", 1986),
    #
    ("Vertigo", 1958),
    #
    ("Toy Story 3", 2010),
    #
    ("M", 1931),
    #
    ("Das Boot", 1981),
    #
    ("A Clockwork Orange", 1971),
    #
    ("Taxi Driver", 1976),
    #
    ("Oldboy", 2003),
    #
    ("Double Indemnity", 1944),
    #
    ("Mononoke-hime", 1997),
    #
    ("Reservoir Dogs", 1992),
    #
    ("Star Wars: Episode VI - Return of the Jedi", 1983),
    #
    ("Once Upon a Time in America", 1984),
    #
    ("To Kill a Mockingbird", 1962),
    #
    ("Requiem for a Dream", 2000),
    #
    ("Braveheart", 1995),
    #
    ("Lawrence of Arabia", 1962),
    #
    ("Hotaru no haka", 1988),
    #
    ("Eternal Sunshine of the Spotless Mind", 2004),
    #
    ("Witness for the Prosecution", 1958),
    #
    ("Full Metal Jacket", 1987),
    #
    ("Singin' in the Rain", 1952),
    #
    ("The Sting", 1973),
    #
    ("Ladri di biciclette", 1948),
    #
    ("Monty Python and the Holy Grail", 1974),
    #
    ("Amadeus", 1984),
    #
    ("All About Eve", 1950),
    #
    ("X-Men: Days of Future Past", 2014),
    #
    ("Snatch", 2000),
    #
    ("Rashômon", 1950),
    #
    ("L.A. Confidential", 1997),
    #
    ("The Treasure of the Sierra Madre", 1948),
    #
    ("The Apartment", 1960),
    #
    ("Some Like It Hot", 1959),
    #
    ("The Third Man", 1949),
    #
    ("Per qualche dollaro in più", 1965),
    #
    ("Indiana Jones and the Last Crusade", 1989),
    #
    ("Inglourious Basterds", 2009),
    #
    ("Jodaeiye Nader az Simin", 2011),
    #
    ("The Kid", 1921),
    #
    ("2001: A Space Odyssey", 1968),
    #
    ("Batman Begins", 2005),
    #
    ("Yôjinbô", 1961),
    #
    ("Unforgiven", 1992),
    #
    ("Metropolis", 1927),
    #
    ("Raging Bull", 1980),
    #
    ("Toy Story", 1995),
    #
    ("Chinatown", 1974),
    #
    ("Scarface", 1983),
    #
    ("The Wolf of Wall Street", 2013),
    #
    ("Up", 2009),
    #
    ("Die Hard", 1988),
    #
    ("Der Untergang", 2004),
    #
    ("The Great Escape", 1963),
    #
    ("Mr. Smith Goes to Washington", 1939),
    #
    ("El laberinto del fauno", 2006),
    #
    ("Taare Zameen Par", 2007),
    #
    ("On the Waterfront", 1954),
    #
    ("The Bridge on the River Kwai", 1957),
    #
    ("Heat", 1995),
    #
    ("Jagten", 2013),
    #
    ("3 Idiots", 2009),
    #
    ("Det sjunde inseglet", 1957),
    #
    ("Smultronstället", 1957),
    #
    ("Ikiru", 1952),
    #
    ("The Elephant Man", 1980),
    #
    ("Ran", 1985),
    #
    ("Tonari no Totoro", 1988),
    #
    ("The General", 1926),
    #
    ("Blade Runner", 1982),
    #
    ("The Gold Rush", 1925),
    #
    ("The Grand Budapest Hotel", 2014),
    #
    ("Lock, Stock and Two Smoking Barrels", 1998),
    #
    ("Good Will Hunting", 1997),
    #
    ("Gran Torino", 2008),
    #
    ("Rebecca", 1940),
    #
    ("El Secreto de sus Ojos", 2009),
    #
    ("The Big Lebowski", 1998),
    #
    ("Casino", 1995),
    #
    ("It Happened One Night", 1934),
    #
    ("Warrior", 2011),
    #
    ("Rush", 2013),
    #
    ("V for Vendetta", 2006),
    #
    ("The Deer Hunter", 1978),
    #
    ("Cool Hand Luke", 1967),
    #
    ("12 Years a Slave", 2013),
    #
    ("Fargo", 1996),
    #
    ("The Maltese Falcon", 1941),
    #
    ("Hauru no ugoku shiro", 2004),
    #
    ("Rang De Basanti", 2006),
    #
    ("Trainspotting", 1996),
    #
    ("Gone with the Wind", 1939),
    #
    ("Into the Wild", 2007),
    #
    ("How to Train Your Dragon", 2010),
    #
    ("Hotel Rwanda", 2004),
    #
    ("Judgment at Nuremberg", 1961),
    #
    ("The Sixth Sense", 1999),
    #
    ("Butch Cassidy and the Sundance Kid", 1969),
    #
    ("A Beautiful Mind", 2001),
    #
    ("The Thing", 1982),
    #
    ("Dial M for Murder", 1954),
    #
    ("Le salaire de la peur", 1953),
    #
    ("Platoon", 1986),
    #
    ("Kill Bill: Vol. 1", 2003),
    #
    ("No Country for Old Men", 2007),
    #
    ("Annie Hall", 1977),
    #
    ("Finding Nemo", 2003),
    #
    ("Mary and Max", 2009),
    #
    ("Sin City", 2005),
    #
    ("Life of Brian", 1979),
    #
    ("Touch of Evil", 1958),
    #
    ("Les Diaboliques", 1955),
    #
    ("Network", 1976),
    #
    ("The Princess Bride", 1987),
    #
    ("Stand by Me", 1986),
    #
    ("Amores perros", 2000),
    #
    ("The Wizard of Oz", 1939),
    #
    ("Incendies", 2010),
    #
    ("The Avengers", 2012),
    #
    ("Ben-Hur", 1959),
    #
    ("There Will Be Blood", 2007),
    #
    ("Her", 2013),
    #
    ("The Grapes of Wrath", 1940),
    #
    ("Les Quatre Cents Coups", 1959),
    #
    ("The Best Years of Our Lives", 1946),
    #
    ("Million Dollar Baby", 2004),
    #
    ("Hachi: A Dog's Tale", 2009),
    #
    ("In the Name of the Father", 1993),
    #
    ("Donnie Darko", 2001),
    #
    ("Otto e Mezzo", 1963),
    #
    ("The Bourne Ultimatum", 2007),
    #
    ("Strangers on a Train", 1951),
    #
    ("Persona", 1966),
    #
    ("Gandhi", 1982),
    #
    ("High Noon", 1952),
    #
    ("The King's Speech", 2010),
    #
    ("Notorious", 1946),
    #
    ("Jaws", 1975),
    #
    ("Kaze no tani no Naushika", 1984),
    #
    ("Infernal Affairs", 2002),
    #
    ("Twelve Monkeys", 1995),
    #
    ("Fanny och Alexander", 1982),
    #
    ("The Terminator", 1984),
    #
    ("Ip Man", 2008),
    #
    ("La strada", 1954),
    #
    ("Stalker", 1979),
    #
    ("Lagaan: Once Upon a Time in India", 2001),
    #
    ("The Night of the Hunter", 1955),
    #
    ("Groundhog Day", 1993),
    #
    ("Harry Potter and the Deathly Hallows: Part 2", 2011),
    #
    ("Rocky", 1976),
    #
    ("Dog Day Afternoon", 1975),
    #
    ("Shutter Island", 2010),
    #
    ("Captain America: The Winter Soldier", 2014),
    #
    ("Who's Afraid of Virginia Woolf?", 1966),
    #
    ("La haine", 1995),
    #
    ("The Big Sleep", 1946),
    #
    ("La battaglia di Algeri", 1965),
    #
    ("Pirates of the Caribbean: The Curse of the Black Pearl", 2003),
    #
    ("Before Sunrise", 1995),
    #
    ("Barry Lyndon", 1975),
    #
    ("Monsters, Inc.", 2001),
    #
    ("Gravity", 2013),
    #
    ("The Graduate", 1967),
    #
    ("Memories of Murder", 2003),
    #
    ("Roman Holiday", 1953),
    #
    ("The Hustler", 1961),
    #
    ("Castle in the Sky", 1986),
    #
    ("Festen", 1998),
    #
    ("Per un pugno di dollari", 1964),
    #
    ("The Help", 2011),
    #
    ("In the Mood for Love", 2000),
    #
    ("A Christmas Story", 1983),
    #
    ("Stalag 17", 1953),
    #
    ("Slumdog Millionaire", 2008),
    #
    ("The Truman Show", 1998),
    #
    ("Swades", 2004),
    #
    ("Underground", 1995),
    #
    ("Rope", 1948),
    #
    ("The Killing", 1956),
    #
    ("Tropa de Elite 2", 2010),
    #
    ("Beauty and the Beast", 1991),
    #
    ("Jurassic Park", 1993),
    #
    ("Black Swan", 2010),
    #
    ("Trois couleurs : Rouge", 1994),
    #
    ("Le scaphandre et le papillon", 2007),
    #
    ("Before Sunset", 2004),
]
