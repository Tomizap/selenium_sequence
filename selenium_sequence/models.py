import random
import re

from colorama import Fore, Style
from pprint import pprint

from selenium_sequence.items import *


def rand():
    return random.randrange(0, 999) * random.randrange(0, 999)


sequences = {
    "indeed": {
        "JOBS": {
            "JOB_URL:get:current_url": {},
            "JOB_NAME:get": "h1 > span",
            "JOB_LOCATION:get": '[data-testid="inlineHeader-companyLocation"]',
            "JOB_DESCRIPTION:get": '#jobDescriptionText',
            "COMPANY_LOCATION:get": '[data-testid="inlineHeader-companyLocation"]',
            # "JOB_SPECIFICATIONS:get": "span.jobsearch-JobMetadataHeader-item",
            "JOB_REQUIREMENTS:get": "#qualificationsSection li > p",
            "JOB_TIME:get": "#mosaic-belowFullJobDescription + .css-q7fux ul li > *:last-child",
            "JOB_ADVANTAGES:get": "#benefits > div",
            "JOB_REVENUE": ".ecydgvn1, #salaryInfoAndJobType > span",
            # "JOB_REVENUE": "#salaryInfoAndJobType > span",
            "JOB_WORKTIME": "#salaryInfoAndJobType > span span",
            "JOB_WORKTIME:get": "#jobDetailsSection > div:last-child > div:last-child",
        },
        "COMPANY": {
            "COMPANY_URL:current_url": {},
            "COMPANY_INDEED_URL:current_url": {},
            "COMPANY_NAME:get": '[data-tn-section="head"] > h1, header > h2',
            "COMPANY_RATING_COUNT:get": 'li[data-tn-element="reviews-tab"] > a > div',
            "COMPANY_JOBS_COUNT:get": 'li[data-tn-element="jobs-tab"] > a > div',
            "COMPANY_CREATION_DATE:get": 'li[data-testid="companyInfo-founded"] > div:last-child',
            "COMPANY_EMPLOYEES_COUNT:get": 'li[data-testid="companyInfo-employee"] > div:last-child',
            "COMPANY_REVENUE:get": 'li[data-testid="companyInfo-revenue"] > div:last-child',
            "COMPANY_SECTOR:get": 'li[data-testid="companyInfo-industry"] > div:last-child',
            "COMPANY_DESCRIPTION:get": '[data-testid="less-text"] p',
            "COMPANY_LOCATION:get": 'li[data-testid="companyInfo-headquartersLocation"] > div:last-child',
            "COMPANY_WEBSITE_URL:get": {
                "selector": 'li[data-testid="companyInfo-companyWebsite"] a',
                "property": "href"
            },
            f":goto_{rand()}": 'li[data-tn-element="interviews-tab"] > a',
            "COMPANY_HIRING_EXPERIENCE:get": '[data-tn-component="summary-experience-card"] > div > div > div:last-child',
            "COMPANY_HIRING_DIFFICULTY:get": '[data-tn-component="summary-difficulty-card"] > div > div > div:last-child',
            "COMPANY_HIRING_TIME:get": '[data-tn-component="summary-hiring-duration-card"] > div > div > div:last-child',
            "COMPANY_PHONE:find:phone": {},
            "COMPANY_EMAIL:find:email": {},
            "COMPANY_WEBSITE_URL:find:website": {},
            "COMPANY_LINKEDIN_URL:find:linkedin": {},
        },
    },
    "linkedin": {
        'COMPANY': {
            ":click_dgsuyd87": ".artdeco-global-alert__body button",
            "COMPANY_NAME:get": "h1 > span",
            "COMPANY_LOCATION:get": ".org-top-card-summary-info-list > .inline-block > div",
            "JOB_LOCATION:get": ".org-top-card-summary-info-list > .inline-block > div",
            "COMPANY_DESCRIPTION:get": "p.org-top-card-summary__tagline",
            "COMPANY_SECTOR:get": ".org-top-card-summary-info-list > div",
            f"COMPANY_EMAIL:find:email": {},
            f"COMPANY_PHONE:find:phone": {},
            # "COMPANY_LINKEDIN_SUSCRIBERS_COUNT:get": ".org-top-card-summary-info-list > .inline-block > div:nth-child(2)",
            "COMPANY_EMPLOYEES_COUNT:get": ".org-top-card-summary-info-list > .inline-block > div + div",
            "COMPANY_WEBSITE_URL:find:website": {},
            "COMPANY_LINKEDIN_URL:find:linkedin": {},
        },
        "JOB": {
            ":click_dgsuyd87": ".artdeco-global-alert__body button",
            "JOB_NAME:get": ".job-view-layout.jobs-details h1",
            "JOB_DESCRIPTION:get": ".job-details > span",
            # "JOB_LOCATION:get": "span.jobs-unified-top-card__bullet",
            "JOB_TIME:get": ".jobs-unified-top-card__primary-description .tvm__text",
            "JOB_APPLICATION_COUNT:get": '.job-details-jobs-unified-top-card__primary-description .tvm__text:last-child',
            "JOB_WORKTIME:get": '.job-details-jobs-unified-top-card__job-insight span + span',
            "JOB_REQUIREMENTS:get": '.job-details-jobs-unified-top-card__job-insight span span:last-child',
            # "JOB_SPECIFICATIONS:get": "ul > li.jobs-unified-top-card__job-insight > span",
        },
        "PEOPLE": {
            ":click_dgsuyd87": ".artdeco-global-alert__body button",
            "PEOPLE_NAME:get": ".pv-text-details__left-panel h1",
            "PEOPLE_NAME:get": ".pv-text-details__left-panel > .text-body-medium",
            ":click": "span.pv-text-details__separator > #top-card-text-details-contact-info",
            ":wait": 3,
            "PEOPLE_BIRTHDAY": "section.pv-contact-info__contact-type.ci-birthday > div",
            "PEOPLE_TWITTER:get": {
                "selector": "section.pv-contact-info__contact-type.ci-twitter > a",
                "property": "href"
            }
        },
        "RECRUITER": {
            ":click_dgsuyd87": ".artdeco-global-alert__body button",
            "RECRUITER_NAME:get": ".pv-text-details__left-panel h1",
            "RECRUITER_NAME:get": ".pv-text-details__left-panel > .text-body-medium",
            ":click": "span.pv-text-details__separator > #top-card-text-details-contact-info",
            ":wait": 3,
            "RECRUITER_EMAIL": "section.pv-contact-info__contact-type.ci-email > div",
            "RECRUITER_BIRTHDAY": "section.pv-contact-info__contact-type.ci-birthday > div",
            "RECRUITER_TWITTER:get": {
                "selector": "section.pv-contact-info__contact-type.ci-twitter > a",
                "property": "href"
            }
        }
    },
    "pole_emploi": {
        "JOBS": {
            "JOB_URL:get:current_url": {},
            "JOB_NAME:get": '[itemprop="title"]',
            "JOB_DESCRIPTION:get": '[itemprop="description"]',
            "JOB_LOCATION:get": '[itemprop="address"], [itemprop="jobLocation"] [itemprop="name"]',
            "JOB_TIME:get": 'span[itemprop="datePosted"]',
            "JOB_SPECIFICATIONS:get": 'div.description-aside dd',
            "JOB_REQUIREMENTS:get": '.skill-list.list-unstyled',
            "JOB_WORKHOURS:get": '[itemprop="workHours"]',
            "JOB_REVENUE:get": '[itemprop="baseSalary"] + ul li',
        },
        "COMPANY": {
            "COMPANY_URL:get:current_url": {},
            "COMPANY_POLE_EMPLOI_URL:get:current_url": {},
            "COMPANY_NAME:get": "h1",
            # "COMPANY_NAME:get": "h1 + p",
            "COMPANY_EMPLOYEES_COUNT:get": ".bloc-illustration > div span > p:last-child",
            "COMPANY_SECTOR:get": ".bloc-illustration > div:last-child span > p:last-child",
            "COMPANY_EMAIL:get": ".vcard-entreprise .vcard-descriptif > p:last-child",
            "COMPANY_WEBSITE_URL:get": ".vcard-entreprise .vcard-descriptif > p:last-child a",
            "COMPANY_EMAIL:find:email": {},
            "COMPANY_PHONE:find:phone": {},
            "COMPANY_WEBSITE_URL:find:website": {},
            "COMPANY_LINKEDIN_URL:find:linkedin": {},
        }
    },
    "hellowork": {
        'JOB': {
            "JOB_NAME:get": '[data-cy="jobTitle"]',
            "COMPANY_JOB:get": "h1.tw-inline + span",
            "COMPANY_NAME:get": ".tw-col-span-full > div > section a",
            "COMPANY_LOCATION:get": "h1.tw-inline + span",
            # "JOB_LOCATION:get": "h1.tw-inline + span",
        },
        'COMPANY': {
            "COMPANY_URL:get:current_url": {},
            "COMPANY_HELLOWORK_URL:get:current_url": {},
            "COMPANY_NAME:get": {
                "selector": ".campagne h1",
                "replace": r'\sRecrutement'
            },
            "COMPANY_LOCATION:get": {
                "selector": ".infos .loc",
                "replace": r'^\w+'
            },
            "COMPANY_SECTOR:get": ".infos .secteur",
            "COMPANY_CREATION_DATE:get": '.infos [data-cy="companyCreationYear"]',
            "COMPANY_EMPLOYEES_COUNT:get": '.infos [data-cy="companyEmployeeNumber"]',
            "COMPANY_REVENUE:get": '.infos [data-cy="companyTurnover"]',
            "COMPANY_LOCATION:get": '.infos .loc',
            "COMPANY_PHONE:find:phone": {},
            "COMPANY_EMAIL:find:email": {},
            "COMPANY_WEBSITE_URL:find:website": {},
            "COMPANY_LINKEDIN_URL:find:linkedin": {},
        }
    },
    'lefigaro': {
        "JOBS": {
            # 'JOB_APPLICATION_COUNT:get': '',    
            'JOB_DESCRIPTION:get': '.job--main--content h2 span',
            'JOB_LOCATION:get': '.jobs-header--info--details img[alt="pin"] + *',
            'JOB_NAME:get': 'h1.jobs-header--info--title',
            'JOB_REQUIREMENTS:get': '.job--main--content > div + div h2 span',
            # 'JOB_REVENUE:get': '',
            'JOB_SPECIFICATIONS:get': '.jobs-header--info--details img[alt="contract"] + *',       
            'JOB_TIME:get': '.jobs-header--info--details img[alt="clock"] + *',
            # 'JOB_NAME:get': '',
            # 'JOB_URL:get': '',
            # 'JOB_WORKSPACE:get': '',
            # 'JOB_WORKTIME:get': '',       
        },
        'COMPANY': {
            # 'COMPANY_APPLICATION_DIFFICULTY:get': '',
            # 'COMPANY_APPLICATION_EXPERIENCE:get': '',
            # 'COMPANY_APPLICATION_TIME:get': '', 
            # 'COMPANY_CREATION_DATE:get': '',
            # 'COMPANY_DESCRIPTION:get': '',      
            # 'COMPANY_EMAIL:get': '',
            'COMPANY_EMPLOYEES_COUNT:get': '.enterprise-header--information--details--stats img[alt="user"] + *',
            # 'COMPANY_JOBS_COUNT:get': '',       
            'COMPANY_LOCATION:get': '.enterprise-header--information--details--location span',
            'COMPANY_NAME:get': '.enterprise-header--information--details--title',
            # 'COMPANY_PHONE:get': '',
            'COMPANY_RATE:get': 'small.star-rating--value__gold',
            # 'COMPANY_REVENUE:get': "",
            'COMPANY_SECTOR:get': '.enterprise-header--information--details--stats--ape span',
            # 'COMPANY_NAME:get': '',
            # 'COMPANY_URL:get': '',
            'COMPANY_EMAIL:find:email': {},
            'COMPANY_PHONE:find:phone': {},
        }
    },
    "labonnealternance": {
        "JOBS": {
            "JOB_NAME:get": "#itemDetailColumn h1",
            "JOB_LOCATION:get": "#itemDetailColumn > header div.css-acwv4d",
            "JOB_DESCRIPTION:get": "#itemDetailColumn div.css-2qrmgs",
            "JOB_TYPE:get": "#itemDetailColumn div.css-rz1orx > div:nth-child(1)",
            "JOB_TIME:get": "#itemDetailColumn div.css-rz1orx > div:nth-child(2)",
            "JOB_WORKTIME:get": "#itemDetailColumn div.css-rz1orx > div:nth-child(4)",
        },
        "COMPANY": {
            "COMPANY_PHONE:find:phone": {},
            "COMPANY_EMAIL:find:email": {},
            "COMPANY_WEBSITE_URL:find:website": {},
            "COMPANY_LINKEDIN_URL:find:linkedin": {},
        }
    }
}

all_models = [
    # ------------------ emploi.lefigaro.fr ------------------
    {
        "website": "emploi.lefigaro.fr",
        "type": "JOBS",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/recherche/offres-emploi"],
        "steps": {
            ":loop": {
                "page": '.v-pagination li:nth-last-child(2)',
                # "page": 1,
                "pagination": '.v-pagination li:last-child',
                "listing": {
                    ":click_ds": "button.button--filled",
                    ":get:all": {
                        "property": "href", 
                        "selector": 'a.search-result-job-card'
                    },
                },
            }
        }
    },
    {
        "website": "emploi.lefigaro.fr",
        "type": "JOBS",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/offres-emploi"],
        "steps": {
            'COMPANY_NAME:get': 'b.jobs-header--info--company--name',
            'COMPANY_LOCATION:get': '.jobs-header--info--details img[alt="pin"] + *',
            'COMPANY_RATE:get': 'small.star-rating--value__gold',
            'COMPANY_EMAIL:find:email': {},
            'COMPANY_PHONE:find:phone': {},
            # ":goto": ":original_url",
            ':sequence_dgsuy': sequences["lefigaro"]['JOBS'],
            ":gotofdf": ":original_url",
            ':gotofd': '.job--main--content__about-company > a',
            ':sequence_dgsds': sequences["lefigaro"]['COMPANY'],
        }
    },
    {
        "website": "emploi.lefigaro.fr",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/entreprises/"],
        "steps": sequences["lefigaro"]['COMPANY']
    },
    # ------------------ lannuaire.service-public.fr ------------------
    {
        "website": "lannuaire.service-public.fr",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/navigation/ile-de-france/mairie"],
        "steps": {
            ":loop": {
                # "pagination": 1,
                "pagination": '#main > div.sp-old > div > div > article > div > div > nav > ul > li:nth-last-child(2) > a',
                "listing": {
                    ":get:all": {"property": "href", "selector": 'ul.list-orga > li > a'},
                    ":click": 'nav.content-pagination > ul > li.active + li a',
                },
            }
        }
    },
    {
        "website": "lannuaire.service-public.fr",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/ile-de-france/"],
        "steps": {
            "NAME:get": 'h1[itemprop="name"]',
            "PHONE:get": "#contentPhone_1",
            "EMAIL:get": 'span[itemprop="email"] > a',
            "WEBSITE": "a#websites",
            "CITY:get": 'p[data-test="address-prop"] > span[itemprop="addressLocality"]',
            "POSTCODE:get": 'p[data-test="address-prop"] > span[itemprop="postalCode"]',
            "ADDRESS:get": 'p[data-test="address-prop"] > span[itemprop="streetAddress"]'
        }
    },

    # ------------------ 123ecoles.com ------------------

    {
        "website": "123ecoles.com",
        "type": "school",
        "require_auth": True,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/etablissements-scolaires-"],
        "steps": {
            ":loop": {
                "pagination": 1,
                # "pagination": 'div.jobs-search-results-list__pagination li:last-child',
                "listing": {
                    ":get:all": {"property": "href", "selector": '.list-group-item > a'},
                },
            }
        }
    },
    {
        "website": "123ecoles.com",
        "type": "school",
        "require_auth": True,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/"],
        "steps": {
            f"COMPANY:get": "body > div.main-wrap > div.main.ts-contain.cf.right-sidebar > div > div > div.the-post-header.s-head-modern.s-head-modern-a.has-share-meta-right > div > h1",
            # f"CONTACT:get": "#post-13703 > div > div > div:nth-child(13) > div",
            f"EMAIL:find:email": "",
            f"PHONE:find:phone": "",
            f"ADDRESS:GET": "#post-13703 > div > div > div:nth-child(15) > div"
        }
    },
    # ------------------ pagesjaunes.fr ------------------
    {
        "website": "pagesjaunes.fr",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/"],
        "steps": {}
    },
    {
        "website": "pagesjaunes.fr",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/"],
        "steps": {}
    },
    # ------------------ linkedin.com ------------------
    # JOBS
    {
        "website": "linkedin.com",
        "type": "JOBS",
        "require_auth": True,
        "fields": JobItem,
        "action": "scrapping",        
        "RegexUrl": ["/jobs/search/"],
        "steps": {
            # ":wait_fdsfsd": 2,
            ":loop": {
                # "page": 1,
                "pagination": 'li.artdeco-pagination__indicator--number.active + li > button',
                "listing": {
                    # ":click": "#ember12",
                    ":execute_script": 'document.querySelector("div.jobs-search-results-list").scroll(0, 999999)',
                    ":get:all": {"property": "href",
                                 "selector": 'div.artdeco-entity-lockup__title > a.job-card-container__link'},
                },
                "deep": True
            }
        }
    },
    
    {
        "website": "linkedin.com",
        "type": "JOB",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/jobs/view"],
        "steps": {
            # JOB
            f":sequence_1": sequences['linkedin']['JOB'],
            f":goto_1": "section.jobs-company a, .jobs-unified-top-card a",
            f":sequence_2": sequences['linkedin']['COMPANY'],
            f":goto_2": ":original_url",
            "RECRUITER_LINKEDIN_URL:get": {
                "selector": ".hirer-card__hirer-information > a.app-aware-link",
                "property": "href"
            },
            f":goto_dssd897": ".hirer-card__hirer-information > a.app-aware-link",
            f":sequence_3": sequences['linkedin']['RECRUITER']
        }
    },
    # COMPANIES
    {
        "website": "linkedin.com",
        "type": "COMPANY",
        "require_auth": True,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/search/results/companies"],
        "steps": {
            ":loop": {
                "pagination": 1,
                "listing": {
                    ":execute_script": 'document.querySelector("html").scroll(0, 9999999)',
                    ":get:all": {"property": "href", "selector": 'span.entity-result__title-text > a.app-aware-link'},
                    ":click": 'ul.artdeco-pagination__pages > li.selected + li',
                },
            }
        }
    },
    {
        "website": "linkedin.com",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping", 
        "RegexUrl": ["/company/"],
        "steps": sequences['linkedin']['COMPANY']
    },
    {
        "website": "linkedin.com",
        "type": "school",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping", 
        "RegexUrl": ["/school/"],
        "steps": sequences['linkedin']['COMPANY']
    },
    # PEOPLE
    {
        "website": "linkedin.com",
        "type": "peoples",
        "require_auth": True,
        "fields": {},
        "actn": "scrapping", 
        "RegexUrl": ["/search/results/people"],
        "steps": {
            ":loop": {
                "pagination": 1,
                "listing": {
                    ":execute_script": 'document.querySelector("html").scroll(0, 9999999)',
                    ":get:all": {"property": "href", "selector": 'span.entity-result__title-text > a.app-aware-link'},
                    ":click": 'ul.artdeco-pagination__pages > li.selected + li',
                },
            }
        }
    },
    {
        "website": "linkedin.com",
        "type": "people",
        "require_auth": False,
        "fields": {},
        "actn": "scrapping", 
        "RegexUrl": ["/in/"],
        "steps": sequences['linkedin']['PEOPLE']
    },
    # ------------------ indeed.com ------------------
    {
        "website": "indeed.com",
        "type": "JOBS",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping", 
        "RegexUrl": ["indeed.com/jobs", "indeed.com/emplois"],
        "steps": {
            ":loop": {
                # "page": 1,
                "pagination": 'a[data-testid="pagination-page-next"]',
                "listing": {
                    ":click_11qsdhyu": "button#onetrust-accept-btn-handler",
                    ":click_12ndsqujf": "#google-Only-Modal > div > div.google-Only-Modal-Upper-Row > button",
                    ":click_13dsq": "h3.DesktopJobAlertPopup-heading + button",
                    ":execute_script": 'document.querySelector("html").scroll(0, 9999999)',
                    ":get:all": {"property": "href", "selector": 'td.resultContent h2 > a'},
                },
                "deep": True
            }
        }
    },
    {
        "website": "indeed.com",
        "type": "JOB",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping", 
        "RegexUrl": ["/viewjob", '/job/', "/pagead/clk", "/rc/clk", "/company/", "/jobs/"],
        "steps": {
            "COMPANY_NAME:get": '[data-testid="inlineHeader-companyName"]',
            "COMPANY_LOCATION:get": '[data-testid="inlineHeader-companyLocation"]',
            ':sequence_job': sequences["indeed"]['JOBS'],
            ":goto": '[data-testid="inlineHeader-companyName"] a',
            ":sequence_company": sequences['indeed']['COMPANY'],
        }
    },
    {
        "website": "indeed.com",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",        
        "RegexUrl": ["/cmp/"],
        "steps": sequences['indeed']['COMPANY']
    },
    # ------------------ candidat.pole-emploi.fr ------------------
    {
        "website": "candidat.pole-emploi.fr",
        "type": "JOBS",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/offres/recherche?"],
        "steps": {
            ":loop": {
                # "page": 1,
                "pagination": "#zoneAfficherPlus a",
                "replace": True,
                "listing": {
                    ":click-cookie": "#footer_tc_privacy_button_2",
                    ":execute_script_1": 'document.querySelector("html").scroll(0, 9999999)',
                    ":click_1": "#zoneAfficherPlus a",
                    ":get:all": {"property": "href", "selector": 'li.result > a.media'}
                },
            }
        }
    },
    {
        "website": "candidat.pole-emploi.fr",
        "type": "JOB",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/offres/recherche/detail/"],
        "steps": {
            "COMPANY_NAME:get": '[itemprop="hiringOrganization"] + h2 + .media .media-body h3',
            "COMPANY_LOCATION:get": '[itemprop="jobLocation"] [itemprop="name"]',    
            ":sequence_dsbuh": sequences['pole_emploi']['JOBS'],
            ":click": '[itemprop="hiringOrganization"] + h2 + .media .media-body p > a',
            ":sequence": sequences['pole_emploi']['COMPANY'],
        }
    },
    {
        "website": "candidat.pole-emploi.fr",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/page-entreprise"],
        "steps": sequences['pole_emploi']['COMPANY']
    },

    # ------------------ labonnealternance.apprentissage.beta.gouv.fr ------------------

    {
        "website": "labonnealternance.apprentissage.beta.gouv.fr",
        "type": "JOB",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["page=", "type=lba"],
        "steps": {
            ":wait": 5,
            "COMPANY_NAME:get": '#itemDetailColumn > header > div > p > span.chakra-text',
            "COMPANY_LOCATION:get": '#itemDetailColumn > header > div > div.css-acwv4d',    
            ":sequence_job": sequences['labonnealternance']['JOBS'],
            ":sequence_company": sequences['labonnealternance']['COMPANY'],
        }
    },
    {
        "website": "labonnealternance.apprentissage.beta.gouv.fr",
        "type": "JOBS",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/recherche-apprentissage"],
        "steps": {
            ":click1": "div.css-1161qt5 > div > div > div > label:nth-child(2) > span.chakra-checkbox__control.css-ildapo",
            ":click2": "div.css-1161qt5 > div > div > div > label:nth-child(3) > span.chakra-checkbox__control.css-ildapo",
            ":wait": 60,
            ":loop": {
                "page": 1,
                "pagination": "body",
                # "replace": True,
                "listing": {
                    ":get:all": {"property": "href", "selector": '#jobList .chakra-link'}
                },
            }
        }
    },

    # ------------------ google.com ------------------

    {
        "website": "google.com",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/maps/place/"],
        "steps": {
            ":click_button": "#content aside a + a, #main aside a + a",
            "COMPANY_NAME:get": 'h1',
            "COMPANY_LOCATION:get": '[data-item-id="address"] .rogA2c',
            "COMPANY_SECTOR:get": "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div:nth-child(2) > span > span > button",
            "COMPANY_PHONE:get": '[data-tooltip="Copier le numéro de téléphone"] .rogA2c',
            "COMPANY_WEBSITE_URL:get": '[data-item-id="authority"] .rogA2c',
            "COMPANY_PHONE:find:phone": {},
            "COMPANY_EMAIL:find:email": {},
            "COMPANY_WEBSITE_URL:find:website": {},
            "COMPANY_LINKEDIN_URL:find:linkedin": {},
        }
    },
    {
        "website": "google.com",
        "type": "COMPANIES",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ['/maps'],
        "steps": {
            ":loop": {
                "page": 50,
                "pagination:not": '[role="feed"] > div.m6QErb.tLjsW',
                "replace": True,
                "listing": {
                    ':wait': 1,
                    ":execute_script": 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd").scroll(0, 999999999)',
                    # ":click_fd": "button#tarteaucitronPersonalize2",
                    ":get:all": {"property": "href", "selector": 'a.hfpxzc'}
                },
            }
        }
    },

    # ------------------ onisep.fr ------------------

    {
        "website": "onisep.fr",
        "type": "SCHOOLS",
        "require_auth": False,
        "fields": SchoolItem,
        "action": "scrapping",
        "RegexUrl": [r"ressources\/univers-formation\/formations\/.{1,}\#etablissements"],
        "steps": {
            ":loop": {
                # "page": 1,
                "pagination": 'nav[role="navigation"] li.search-header-pagination-next',
                # "replace": True,
                "listing": {
                    ":click_fd": "button#tarteaucitronPersonalize2",
                    ":get:all": {"property": "href", "selector": '#etablissements div.search-ui-result-outer table a'}
                },
            }
        }
    },
    {
        "website": "onisep.fr",
        "type": "SCHOOL",
        "require_auth": False,
        "fields": SchoolItem,
        "action": "scrapping",
        "RegexUrl": [
            "/ressources/Univers-Lycee/", 
            "/ressources/Univers-Postbac/"],
        "steps": {
            ":click_button": "#content aside a + a, #main aside a + a",
            "SCHOOL_NAME:get": "h1",
            "SCHOOL_LOCATION:get": "#adresse .callout-text + div > span + span",
            "SCHOOL_PHONE:get": "#contact .callout-text span",
            "SCHOOL_WEBSITE:get": "#contact .callout-text a",
            "SCHOOL_EMAIL:get": "#contact .callout-text + div a",
        }
    },

    # ------------------ hellowork.com ------------------

    {
        "website": "hellowork.com",
        "type": "JOBS",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/emploi/recherche.html?"],
        "steps": {
            ":loop": {
                # "page": 1,
                "pagination": "#pagin > div > div > div:nth-child(2) > div > ul > li.next",
                "replace": False,
                "listing": {
                    ":click-cookie": "#hw-cc-notice-accept-btn",
                    # ":execute_script_1": 'document.querySelector("html").scroll(0, 9999999)',
                    # ":click_1": "#zoneAfficherPlus a",
                    ":get:all": {"property": "href", "selector": '.offer--content a'}
                },
            }
        }
    },
    {
        "website": "hellowork.com",
        "type": "JOB",
        "require_auth": False,
        "fields": JobItem,
        "action": "scrapping",
        "RegexUrl": ["/emplois/"],
        "steps": {
            ":sequence_job": sequences["hellowork"]['JOB'],
            # "COMPANY_HELLOWORK:get": {
            #     'selector': '.tw-col-span-full > div > section a',
            #     'property': "href"
            # },
            ":goto_dbs": '.tw-col-span-full > div > section a',
            ":sequence_re": sequences["hellowork"]['COMPANY'],
            ":goto_534r": ":original_url"
        }
    },
    {
        "website": "hellowork.com",
        "type": "COMPANY",
        "require_auth": False,
        "fields": CompanyItem,
        "action": "scrapping",
        "RegexUrl": ["/entreprise/", '/entreprises/'],
        "steps": sequences['hellowork']['COMPANY']
    },
]


def find_model(url=None, action=None) -> dict:
    models = all_models
    if action is None:
        action = 'scrapping'

    if url is None:
        return {
            "message": 'No url provided',
            "steps": {}
        }
    # print(Fore.WHITE + 'find_model()')
    for model in models:
        if model['website'] in url:
            for regex in model['RegexUrl']:
                if regex in url or bool(re.search(regex, url)):
                    # print(Fore.GREEN + 'model founded')
                    # pprint(model)
                    # print(Style.RESET_ALL)
                    return model
                else:
                    pass
        else:
            pass
    # print(url)
    print(Fore.RED + f'Aucun modèle: {url}')
    print(Style.RESET_ALL)
    return {
        "ok": False,
        "message": 'No model found',
        "steps": {}
    }



# pprint(find_model(url=f"https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?display=list&page=fiche&type=matcha&itemId=6511781e6bcb57308f5d223f&job_name=Secr%C3%A9tariat%20m%C3%A9dical&romes=J1303,M1609,M1607&radius=60&lat=48.784506&lon=2.452976&zipcode=94000&insee=94028&address=Cr%C3%A9teil%2094000 "))