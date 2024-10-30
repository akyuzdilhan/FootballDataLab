from dash import html, dcc

CARDS_FOLDER = "/assets/cardsLogo/"

sections = [
    {
        'title': 'Data Providers', 'icon': CARDS_FOLDER + 'data-providers.png', 'link': '/data-providers',
        'description': ['Major Data Providers', 'Data Collection Methods', 'Tools for Data Manipulation and Visualization', 'AI and Automation']
    },
    {
        'title': 'Governing Bodies', 'icon': CARDS_FOLDER + 'governing-bodies.png', 'link': '/governing-bodies',
        'description': ['Performance Monitoring', 'Integrity and Anti-Match Fixing', 'Game Development', 'Tournament and Fixture Management'],
    },
    {
        'title': 'Football Clubs and Coaching Staff', 'icon': CARDS_FOLDER + 'football-club.png', 'link': '/clubs',
        'description': ['Scouting and Recruitment', 'Player Performance and Tactical Analysis', 'Training Optimization', 'Player Selection and Rotation']
    },
    {
        'title': 'Players', 'icon': CARDS_FOLDER + 'player.png', 'link': '/payers',
        'description': ['Contract Negotiations and Career Planning', 'Transfer Decision-Making', 'Opposition and Match Preparation', 'Personal Skill Development'],
    },
    {
        'title': 'Football Analysts and Data Scientists', 'icon': CARDS_FOLDER + 'football-analyst.png', 'link': '/analysts',
        'description': ['Advanced Metrics Development', 'Predictive Modeling', 'Visualization and Communication', 'Machine Learning Applications'], 
    },
    {
        'title': 'Sports Scientists and Medical Teams', 'icon': CARDS_FOLDER + 'sport-scientist.png', 'link': '/scientists',
        'description': ['Injury Prevention', 'Load Management', 'Recovery Protocols', 'Psychological Monitoring'],
    },
    {
        'title': 'Broadcasters and Media', 'icon': CARDS_FOLDER + 'broadcast2.png', 'link': '/media',
        'description': ['Live Match Analysis', 'Data-Driven Storytelling', 'Fantasy Sports and Interactive Features'], 
    },
    {
        'title': 'Fans and Enthusiasts', 'icon': CARDS_FOLDER + 'fan.png', 'link': '/fans',
        'description': ['Social Media and Community Contributions', 'Fan Analysis Platforms', 'Independent Projects'], 
    },
    {
        'title': 'Sports Betting Platforms', 'icon': CARDS_FOLDER + 'betting-platforms.png', 'link': '/betting',
        'description': ['Player Projections', 'Match Outcome Predictions', 'Risk Assessment'], 
    }
]

layout = html.Div([
    html.Div(
        style={
            'backgroundImage': 'url("/assets/dataFootWallpaper.jpg")',
            'backgroundSize': 'cover',
            'backgroundPosition': 'center',
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '60vh',
            'filter': 'brightness(70%)',
            'zIndex': '-1'
        }
    ),
    html.Div(
        style={
            'width': '100%',
            'height': '45vh',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center',
            'color': '#f8f5f0',
            'textAlign': 'center',
            'textShadow': '2px 2px 5px rgba(0, 0, 0, 0.8)'
        },
        children=[
            html.H1("The Football\nData Science Laboratory", style={
                'fontSize': '80px', 'fontWeight': 'bold', 'margin': '0', 'whiteSpace': 'pre-wrap'
            }),
            html.H3("Search, Understand and Share the knowledge\nof Football Data", style={
                'fontSize': '40px', 'fontWeight': 'bold', 'marginTop': '40px', 'marginBottom': '40px', 'whiteSpace': 'pre-wrap'
            }),
            dcc.Link(
                html.Button("Explore on GitHub", style={
                    'padding': '12px 30px', 'fontSize': '20px', 'backgroundColor': '#44A3DB', 'color': '#f8f5f0', 'fontWeight': 'bold', 'border': 'none', 'borderRadius': '15px', 'cursor': 'pointer'
                }),
                href="https://github.com/akyuzdilhan/FootballDataLab", target="_blank"
            )
        ]
    ),

    html.Div(
        style={
            'padding': '120px 40px 30px 40px',
            'textAlign': 'center',
            'maxWidth': '1150px',
            'margin': 'auto',
            'color': '#333',
        },
        children=[
            html.H2("The Role of Data in Modern Football", style={
                'fontSize': '36px', 'fontWeight': 'bold', 'marginBottom': '20px'
            }),
            html.P("Football, a sport with nearly 200 years of history, has always been defined by passion, strategy, and skill. In recent decades, however, data has emerged as a transformative tool, reshaping the game. Inspired by the success of analytics in American sports like baseball and basketball, the football world began embracing data in the early 2000s, marking the start of a new era.",
                   style={'fontSize': '18px', 'lineHeight': '1.6', 'marginBottom': '20px'}),
            html.P("Today, data permeates every aspect of the sport, driving decisions at all levels. The exponential growth in data and technology has empowered clubs, analysts, and media to extract deeper insights, making football more strategic and engaging for fans worldwide.",
                   style={'fontSize': '18px', 'lineHeight': '1.6'})
        ]
    ),
    
    html.Div(
        style={
            'padding': '60px 160px',
            'textAlign': 'center',
            'backgroundColor': '#f8f5f0',
            'width': '99vw',
            'borderTop': '2px solid #dedede',
            'borderBottom': '2px solid #dedede'
        },
        children=[
            html.Div(
                style={
                    'margin': 'auto',
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
                    'gap': '30px',
                    'alignItems': 'stretch', 
                },
                children=[
                    dcc.Link(
                        html.Div(
                            style={
                                'backgroundColor': 'white',
                                'backdropFilter': 'blur(10px)',
                                'boxShadow': '0 8px 16px rgba(0, 0, 0, 0.2)',
                                'padding': '30px 30px 0px 30px',
                                'borderRadius': '10px',
                                'border': '1px solid black',
                                'textAlign': 'center',
                                'height': '100%',
                                'transition': 'transform 0.3s ease',
                                'fontFamily': '"Poppins", sans-serif',
                                'display': 'flex',
                                'flexDirection': 'column', 
                            },
                            children=[
                                html.Img(src=section['icon'], style={'width': '50px', 'height': '50px', 'marginBottom': '500px', 'display': 'block', 'margin': '0 auto'}),
                                html.H3(section['title'], style={'fontSize': '24px', 'fontWeight': 'bold'}),
                                html.Ul(
                                    [html.Li(desc) for desc in section['description']],
                                    style={'listStyleType': 'none', 'padding': '0'}
                                ),
                            ], className='card'
                        ), href=section['link'], style={'textDecoration': 'none', 'color': 'inherit'}
                    ) for section in sections
                ]
            )
        ]
    ),

    html.Div(
        style={
            'position': 'relative',
            'padding': '60px 0',
            'backgroundImage': 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("/assets/background/foot-ai.jpg")',
            'backgroundSize': 'cover',
            'backgroundPosition': 'center',
            'color': '#f8f5f0',
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'flex-start'
        },
        children=[
            #html.Div(
                #style={
                    #maxWidth': '600px',
                    #'padding': '40px 20px',
                    #'textAlign': 'left',
                    #'zIndex': '1'
                #},
                #children=[
                #    html.Img(src='/assets/background/analytics-mockup-1.png', style={'width': '120px', 'transform': 'rotate(-3deg)', 'boxShadow': '0 8px 16px rgba(0,0,0,0.3)'}),
                #    html.Img(src='/assets/background/branding-opta.jpg', style={'width': '120px', 'transform': 'rotate(5deg)', 'boxShadow': '0 8px 16px rgba(0,0,0,0.3)'}),
                #    html.Img(src='/assets/background/Pass-Predictions.png', style={'width': '120px', 'transform': 'rotate(5deg)', 'boxShadow': '0 8px 16px rgba(0,0,0,0.3)'}),
                #]
            #),
            html.Div(
                style={
                    'maxWidth': '1400px',
                    'padding': '40px 20px 40px 150px',
                    'textAlign': 'left',
                    'zIndex': '1'
                },
                children=[
                    html.H2("The Evolving Role of Data in Football", style={'fontSize': '36px', 'marginBottom': '0px'}),
                    html.P(
                        "While football has historically lagged behind American sports in embracing data analytics, the sport is now undergoing a transformation. The complexity of the game, continuous flow, and reliance on intuition have posed challenges for real-time data analysis.",
                        style={'fontSize': '20px', 'lineHeight': '1.6', 'marginBottom': '20px'}
                    ),
                    html.H3("Bridging the Gap with Analytics", style={'fontSize': '28px', 'marginBottom': '0px'}),
                    html.P(
                        "With advances in tracking technologies, predictive modeling, and machine learning, clubs can now make smarter decisions in player recruitment, tactical planning, and injury prevention.",
                        style={'fontSize': '21px', 'lineHeight': '1.6', 'marginBottom': '20px'}
                    ),
                    html.H3("Contributing to the Future of Football", style={'fontSize': '28px', 'marginBottom': '0px'}),
                    html.P(
                        "My goal with this project is to demystify football data and inspire further innovation. By bridging the gap between traditional approaches and advanced analytics, I aim to help football become a leader in data-driven decision-making.",
                        style={'fontSize': '21px', 'lineHeight': '1.6'}
                    )
                ]
            )
        ]
    )
])