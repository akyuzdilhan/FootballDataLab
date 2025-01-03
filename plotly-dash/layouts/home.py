from dash import html, dcc, callback, Output, Input, State, ALL
import dash_bootstrap_components as dbc

CARDS_FOLDER = "/assets/cardsLogo/"

sections = [
    {
        'title': 'Data Providers',
        'icon': CARDS_FOLDER + 'data-providers.png',
        'description': ['Major Data Providers', 'Data Collection Methods', 'Tools for Data Manipulation and Visualization', 'AI and Automation'],
        'content_markdown_file': 'assets/markdown/data_providers.md'
    },
    {
        'title': 'Governing Bodies', 'icon': CARDS_FOLDER + 'governing-bodies.png',
        'description': ['Performance Monitoring', 'Integrity and Anti-Match Fixing', 'Game Development', 'Tournament and Fixture Management'],
        'content_markdown_file': 'assets/markdown/governing_bodies.md'
    },
    {
        'title': 'Football Clubs and Coaching Staff', 'icon': CARDS_FOLDER + 'football-club.png',
        'description': ['Scouting and Recruitment', 'Player Performance and Tactical Analysis', 'Training Optimization', 'Player Selection and Rotation'],
        'content_markdown_file': 'assets/markdown/football_clubs_and_coaching_staff.md'
    },
    {
        'title': 'Players', 'icon': CARDS_FOLDER + 'player.png',
        'description': ['Contract Negotiations and Career Planning', 'Transfer Decision-Making', 'Opposition and Match Preparation', 'Personal Skill Development'],
        'content_markdown_file': 'assets/markdown/players.md'
    },
    {
        'title': 'Football Analysts and Data Scientists', 'icon': CARDS_FOLDER + 'football-analyst.png',
        'description': ['Advanced Metrics Development', 'Predictive Modeling', 'Visualization and Communication', 'Machine Learning Applications'], 
        'content_markdown_file': 'assets/markdown/football_analysts_and_data_scientists.md'
    },
    {
        'title': 'Sports Scientists and Medical Teams', 'icon': CARDS_FOLDER + 'sport-scientist.png',
        'description': ['Injury Prevention', 'Load Management', 'Recovery Protocols', 'Psychological Monitoring'],
        'content_markdown_file': 'assets/markdown/sports_scientists_and_medical_teams.md'
    },
    {
        'title': 'Broadcasters and Media', 'icon': CARDS_FOLDER + 'broadcast2.png',
        'description': ['Live Match Analysis', 'Data-Driven Storytelling', 'Fantasy Sports and Interactive Features'], 
        'content_markdown_file': 'assets/markdown/broadcasters_and_media.md'
    },
    {
        'title': 'Fans and Enthusiasts', 'icon': CARDS_FOLDER + 'fan.png',
        'description': ['Social Media and Community Contributions', 'Fan Analysis Platforms', 'Independent Projects'], 
        'content_markdown_file': 'assets/markdown/fans_and_enthusiasts.md'
    },
    {
        'title': 'Sports Betting Platforms', 'icon': CARDS_FOLDER + 'betting-platforms.png',
        'description': ['Player Projections', 'Match Outcome Predictions', 'Risk Assessment'], 
        'content_markdown_file': 'assets/markdown/sports_betting_platforms.md'
    }
]

layout = html.Div([
    html.Div(className='hero-background'),
    
    html.Div(className='hero-content', children=[
        html.H1("The Football\nData Science Laboratory", className='hero-title'),
        html.H3("Search, Understand and Share the knowledge\nof Football Data", className='hero-subtitle'),
        dcc.Link(
            html.Button("Explore on GitHub", className='hero-button'),
            href="https://github.com/akyuzdilhan/FootballDataLab", target="_blank"
        )
    ]),

    html.Div(className='intro-section', children=[
        html.H2("The Role of Data in Modern Football", className='intro-title'),
        html.P(
            "Football, a sport with nearly 200 years of history, has always been defined by passion, strategy, and skill. In recent decades, however, data has emerged as a transformative tool, reshaping the game. Inspired by the success of analytics in American sports like baseball and basketball, the football world began embracing data in the early 2000s, marking the start of a new era.",
            className='intro-text'
        ),
        html.P(
            "Today, data permeates every aspect of the sport, driving decisions at all levels. The exponential growth in data and technology has empowered clubs, analysts, and media to extract deeper insights, making football more strategic and engaging for fans worldwide.",
            className='intro-text'
        )
    ]),
    
    html.Div(className='cards-section', children=[
        html.Div(className='cards-grid', children=[
            html.Div(
                id={'type': 'open-modal', 'index': section['title']},
                n_clicks=0,
                className='card',
                children=[
                    html.Img(src=section['icon'], className='card-icon'),
                    html.H3(section['title'], className='card-title'),
                    html.Ul(
                        [html.Li(desc, className='card-desc-item') for desc in section['description']],
                        className='card-desc-list'
                    ),
                ]
            ) for section in sections
        ])
    ]),

    dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(id='modal-title'),
                close_button=True,
                className='modal-header-custom'
            ),
            dbc.ModalBody(
                id='modal-body',
                className='modal-body-custom'
            ),
        ],
        id='modal',
        is_open=False,
        className='custom-modal',
        centered=True,
        scrollable=True,
    ),

    html.Div(
        className='final-section',
        children=[
            html.Div(
                className='final-content',
                children=[
                    html.H2("The Evolving Role of Data in Football", className='final-title'),
                    html.P(
                        "While football has historically lagged behind American sports in embracing data analytics, the sport is now undergoing a transformation. The complexity of the game, continuous flow, and reliance on intuition have posed challenges for real-time data analysis.",
                        className='final-text'
                    ),
                    html.H3("Bridging the Gap with Analytics", className='final-subtitle'),
                    html.P(
                        "With advances in tracking technologies, predictive modeling, and machine learning, clubs can now make smarter decisions in player recruitment, tactical planning, and injury prevention.",
                        className='final-text'
                    ),
                    html.H3("Contributing to the Future of Football", className='final-subtitle'),
                    html.P(
                        "My goal with this project is to demystify football data and inspire further innovation. By bridging the gap between traditional approaches and advanced analytics, I aim to help football become a leader in data-driven decision-making.",
                        className='final-text'
                    )
                ]
            )
        ]
    )
])