* First, I would like to apologize for not finishing up my assignments. I still have hard time understanding the visualization (using flask) part*

SI507F17_finalproject.py includes: Cached pages, Setting up databases, Visualization

Important:

- Two cached pages : Most popular fonts, Hot web fonts
- Website: https://www.fontsquirrel.com/
- Purpose: Getting comprehesive lists of fonts (only sans serif, serif, slab serif) that are popular and also trendy from this website 
- Contents : Font name, Image of the fonts, Font styles and number of the font styles
- Flask: http://localhost:8080/
- Help: Stella Choi and Kenji Kaneko 

Others:

- Cached pages are in the "cache_file.json"
- DB information is in "config.py"
- Version of Python : Python3
- No need for key and secret

Citations:

- Cache: section-week-6 
- Flask: 507 Project 6.5 templates folder ('values.html')
- Database: chinook_database.py

How it works:

In order to get these contents using Beautifulsoup,
1. Limited to 20 fonts for both pages
    1. Too many lists of fonts in one page
2. Sorted these fonts by classifications
    1. Looped in three_fonts = ['sans serif', 'serif', 'slab serif’]
    2. Most_popular_fonts = line 143-172
    3. Hot_web_fonts = line 179- 203

Connected two classes (Font, Top Fonts) for database table
- add_font functions 
    - If the font name appears on the ‘Most popular’ page, it appends into popular_fonts list 
        - Categorized into ‘popular’
    - If the font name appears on the ‘Hot web’ page, it appends into hot_fonts list
        - Categorized into ‘trend’  


Expectations for visualization:
- It only has the popular_font_list
	- Supposedly, wanted to have popular_font_list and hot_font_list aligned together as well as fonts' images
