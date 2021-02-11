hover_dict = {'C1_School closing': {'None':'None',
									'Medium':'Recommend closing or all schools open with alterations resulting in significant differences compared to non-Covid-19 operations',
									'Medium-Hard': 'Require closing (only some levels or categories, eg just high school, or just public schools',
									'Hard' : 'Require closing (only some levels or categories, eg just high school, or just public schools',
									'Strict': 'Require closing all levels'},
			'C2_Workplace closing': {'None':'None',
									'Medium':'Recommend closing (or recommend work from home)',
									'Medium-Hard': 'Require closing (or work from home) for some sectors or categories of workers',
									'Hard' : 'Require closing (or work from home) for some sectors or categories of workers',
									'Strict': 'Require closing (or work from home) for all-but-essential workplaces (eg grocery stores, doctors)'},
			'C3_Cancel public events': {'None':'None','Medium':'recommend cancelling',
										'Medium-Hard': 'Require cancelling',
										'Hard' : 'Require cancelling',
										'Strict': 'Require cancelling'},
			'C4_Restrictions on gatherings':  {'None':'None','Medium':'restrictions on very large gatherings (the limit is above 1000 people)',
												'Medium-Hard': 'Restrictions on gatherings between 101-1000 people',
												'Hard' : 'Restrictions on gatherings between 11-100 people',
												'Strict': 'Restrictions on gatherings of 10 people or less'},
			'C5_Close public transport': {'None':'None','Medium':' recommend closing (or significantly reduce volume/route/means of transport available)',
											'Medium-Hard': 'Require closing (or prohibit most citizens from using it)',
											'Hard' : 'Require closing (or prohibit most citizens from using it)',
											'Strict': 'Require closing (or prohibit most citizens from using it)'},
			'C6_Stay at home requirements': {'None':'None','Medium':'Recommend not leaving house',
											'Medium-Hard': 'Require not leaving house with exceptions for daily exercise, grocery shopping, and \'essential\' trips',
											'Hard' : 'Require not leaving house with minimal exceptions (e.g. allowed to leave once a week, or only one person can leave at a time, etc)',
											'Strict': 'Require not leaving house with minimal exceptions (e.g. allowed to leave once a week, or only one person can leave at a time, etc)'},
			'C7_Restrictions on internal movement': {'None':'None','Medium':' Recommend not to travel between regions/cities',
													'Medium-Hard': 'Internal movement restrictions in place',
													'Hard' : 'Internal movement restrictions in place',
													'Strict': 'Internal movement restrictions in place'},
			'C8_International travel controls': {'None':'None','Medium':'Screening arrivals',
												'Medium-Hard': 'Quarantine arrivals from some or all regions',
												'Hard' : 'Ban arrivals from some regions',
												'Strict': 'Ban on all regions or total border closure'},
			'H1_Public information campaigns':{'None':'None','Medium':'Public officials urging caution about COVID-19',
												'Medium-Hard': 'coordinated public information campaign (eg across traditional and social media)',
												'Hard' : 'Coordinated public information campaign (e.g. across traditional and social media)',
												'Strict': 'Coordinated public information campaign (e.g. across traditional and social media)'},
			'H2_Testing policy':  {'None':'None','Medium':'Only those who both (a) have symptoms AND (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)',
									'Medium-Hard': 'Testing of anyone showing Covid-19 symptoms',
									'Hard' : 'Open public testing (eg "drive through" testing available to asymptomatic people)',
									'Strict': 'Open public testing (eg "drive through" testing available to asymptomatic people)'},
			'H3_Contact tracing': {'None':'None','Medium':'Limited contact tracing; not done for all cases',
									'Medium-Hard': 'Comprehensive contact tracing; done for all identified cases',
									'Hard' : 'Comprehensive contact tracing; done for all identified cases',
									'Strict': 'Comprehensive contact tracing; done for all identified cases'},
			'H6_Facial Coverings': {'None':'None','Medium':'Recommended',
									'Medium-Hard': 'Required in some specified shared/public spaces outside the home with other people present, or some situations when social distancing not possible',
									'Hard' : 'Required in all shared/public spaces outside the home with other people present or all situations when social distancing not possible',
									'Strict': 'Required outside the home at all times regardless of location or presence of other people'},
			'H7_Vaccination Policy': {'None':'None','Medium':'Availability for ONE of following: key workers/ clinically vulnerable groups / elderly groups',
									'Medium-Hard': 'Availability for TWO of following: key workers/ clinically vulnerable groups / elderly groups',
									'Hard' : 'Availability for ALL of following: key workers/ clinically vulnerable groups / elderly groups',
									'Strict': 'Universal availability'},
			'E1_Income support': {'None':'No income support',
								'Medium-Hard': 'Government is replacing less than 50 percent of lost salary (or if a flat sum, it is less than 50 percent median salary)',
								'Medium': 'Government is replacing 50 percent or more of lost salary (or if a flat sum, it is greater than 50 percent median salary)'},
			'E2_Debt/contract relief': {'None': 'No debt/contract relief',
										'Medium-Hard': 'narrow relief, specific to one kind of contract',
										'Medium': 'broad debt/contract relief'},
									}