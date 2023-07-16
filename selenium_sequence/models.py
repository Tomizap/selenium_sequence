import random

from colorama import Fore, Style
from pprint import pprint


def rand():
    return random.randrange(0, 999) * random.randrange(0, 999)


sequences = {
    "indeed": {
        "COMPANY": {
            "COMPANY_NAME:get": 'header > h2',
            "COMPANY_RATE:get": 'li[data-tn-element="reviews-tab"] > a > div',
            "COMPANY_JOBS_COUNT:get": 'li[data-tn-element="jobs-tab-tab"] > a > div',
            "COMPANY_CREATION_DATE:get": 'li[data-testid="companyInfo-founded"] > div:last-child',
            "COMPANY_EMPLOYEES_COUNT:get": 'li[data-testid="companyInfo-employee"] > div:last-child',
            "COMPANY_REVENUE:get": 'li[data-testid="companyInfo-revenue"] > div:last-child',
            "COMPANY_SECTOR:get": 'li[data-testid="companyInfo-industry"] > div:last-child',
            "COMPANY_LOCATION:get": 'li[data-testid="companyInfo-headquartersLocation"] > div:last-child',
            # COMPANY EMAIL
            "COMPANY_WEBSITE:get": {
                "selector": 'li[data-testid="companyInfo-companyWebsite"] a',
                "property": "href"
            },
            # APPLICATION
            f":goto_{rand()}": 'li[data-tn-element="interviews-tab"] > a',
            "COMPANY_APPLICATION_EXPERIENCE:get": '[data-tn-component="summary-experience-card"] > div > div > div:last-child',
            "COMPANY_APPLICATION_DIFFICULTY:get": '[data-tn-component="summary-difficulty-card"] > div > div > div:last-child',
            "COMPANY_APPLICATION_TIME:get": '[data-tn-component="summary-hiring-duration-card"] > div > div > div:last-child',
        },
        "RECRUITER": {

        }
    },
    "linkedin": {
        'COMPANY': {
            "COMPANY_NAME:get": "h1 > span",
            "COMPANY_TITLE:get": "h1 > span",
            "COMPANY_LOCATION:get": ".org-top-card-summary-info-list > .inline-block > div",
            "COMPANY_SHORT_DESCRIPTION:get": "p.org-top-card-summary__tagline",
            "COMPANY_SECTOR:get": ".org-top-card-summary-info-list > div",
            f":find:email": {
                "name": "h1 > span",
                "title": ".org-top-card-summary-info-list > div",
                "location": ".org-top-card-summary-info-list > .inline-block > div",
                "property": "COMPANY_EMAIL"
            },
            f":find:phone": {
                "name": "h1 > span",
                "title": ".org-top-card-summary-info-list > div",
                "location": ".org-top-card-summary-info-list > .inline-block > div",
                "property": "COMPANY_PHONE"
            },
            "COMPANY_LINKEDIN_SUSCRIBERS_COUNT:get": ".org-top-card-summary-info-list > .inline-block > div:nth-child(2)",
            "COMPANY_EMPLOYEES_COUNT:get": ".org-top-card-summary-info-list > .inline-block > div:nth-child(3)",
            f":click_{rand()}": "ul.org-page-navigation__items > li:nth-child(2)",
            f":wait_{rand()}": 2,
            "COMPANY_WEBSITE:get": "dl > dd a"
        },
        "JOB": {
            "JOB_NAME:get": "h1",
            "JOB_LOCATION:get": "span.jobs-unified-top-card__bullet",
            "JOB_TIME:get": "span.jobs-unified-top-card__posted-date",
            "JOB_WORKSPACE:get": "span.jobs-unified-top-card__workplace-type",
            "JOB_APPLICATION_COUNT:get": "span.jobs-unified-top-card__applicant-count",
            "JOB_SPECIFICATIONS:get": "ul > li.jobs-unified-top-card__job-insight > span",
        },
        "PEOPLE": {
            "PEOPLE_NAME:get": ".pv-text-details__left-panel h1",
            "PEOPLE_TITLE:get": ".pv-text-details__left-panel > .text-body-medium",
            ":click": "span.pv-text-details__separator > #top-card-text-details-contact-info",
            ":wait": 3,
            "PEOPLE_BIRTHDAY": "section.pv-contact-info__contact-type.ci-birthday > div",
            "PEOPLE_TWITTER:get": {
                "selector": "section.pv-contact-info__contact-type.ci-twitter > a",
                "property": "href"
            }
        },
        "RECRUITER": {
            "RECRUITER_NAME:get": ".pv-text-details__left-panel h1",
            "RECRUITER_TITLE:get": ".pv-text-details__left-panel > .text-body-medium",
            ":click": "span.pv-text-details__separator > #top-card-text-details-contact-info",
            ":wait": 3,
            "RECRUITER_EMAIL": "section.pv-contact-info__contact-type.ci-email > div",
            "RECRUITER_BIRTHDAY": "section.pv-contact-info__contact-type.ci-birthday > div",
            "RECRUITER_TWITTER:get": {
                "selector": "section.pv-contact-info__contact-type.ci-twitter > a",
                "property": "href"
            }
        }
    }
}

all_models = [
    # --- lannuaire.service-public.fr ---
    {
        "website": "lannuaire.service-public.fr",
        "type": "city_halls",
        "require_auth": False,
        "RegexUrl": ["/navigation/ile-de-france/mairie"],
        "sequence": {
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
        "type": "item",
        "require_auth": False,
        "RegexUrl": ["/ile-de-france/"],
        "sequence": {
            "NAME:get": 'h1[itemprop="name"]',
            "PHONE:get": "#contentPhone_1",
            "EMAIL:get": 'span[itemprop="email"] > a',
            "WEBSITE": "a#websites",
            "CITY:get": 'p[data-test="address-prop"] > span[itemprop="addressLocality"]',
            "POSTCODE:get": 'p[data-test="address-prop"] > span[itemprop="postalCode"]',
            "ADDRESS:get": 'p[data-test="address-prop"] > span[itemprop="streetAddress"]'
        }
    },
    # --- google.com ---
    {
        "website": "google.com",
        "type": "city_halls",
        "RegexUrl": ["/maps/search"],
        "sequence": {
            ":googlemaps": {

            }
        }
    },
    # --- pagesjaunes.fr ---
    {
        "website": "pagesjaunes.fr",
        "type": "city_halls",
        "require_auth": False,
        "RegexUrl": ["/"],
        "sequence": {}
    },
    {
        "website": "pagesjaunes.fr",
        "type": "item",
        "require_auth": False,
        "RegexUrl": ["/"],
        "sequence": {}
    },
    # --- linkedin.com ---
    # JOBS
    {
        "website": "linkedin.com",
        "type": "jobs",
        "require_auth": True,
        "RegexUrl": ["/jobs/search"],
        "sequence": {
            ":loop": {
                "pagination": 1,
                # "pagination": 'div.jobs-search-results-list__pagination li:last-child',
                "listing": {
                    ":execute_script": 'document.querySelector("div.jobs-search-results-list").scroll(0, 999999)',
                    ":get:all": {"property": "href",
                                 "selector": 'div.artdeco-entity-lockup__title > a.job-card-container__link'},
                    ":click": 'div.jobs-search-results-list__pagination li.selected + li',
                },
            }
        }
    },
    {
        "website": "linkedin.com",
        "type": "job",
        "require_auth": True,
        "RegexUrl": ["/jobs/view"],
        "sequence": {
            # JOB
            f":sequence_1": sequences['linkedin']['JOB'],
            ":wait_31": 2,
            # COMPANY
            "COMPANY_LINKEDIN:get": {
                "selector": "section.jobs-company a, .jobs-unified-top-card a",
                "property": "href"
            },
            f":goto_1": "section.jobs-company a, .jobs-unified-top-card a",
            f":sequence_2": sequences['linkedin']['COMPANY'],
            f":goto_2": ":original_url",
            ":wait_3438": 2,
            # RECRUITER
            "RECRUITER_LINK:get": {
                "selector": ".hirer-card__hirer-information > a.app-aware-link",
                "property": "href"
            },
            f":goto_{rand()}": ".hirer-card__hirer-information > a.app-aware-link",
            f":sequence_3": sequences['linkedin']['RECRUITER']
        }
    },
    # COMPANIES
    {
        "website": "linkedin.com",
        "type": "companies",
        "require_auth": True,
        "RegexUrl": ["/search/results/companies"],
        "sequence": {
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
        "type": "company",
        "require_auth": True,
        "RegexUrl": ["/company/"],
        "sequence": sequences['linkedin']['COMPANY']
    },
    {
        "website": "linkedin.com",
        "type": "school",
        "require_auth": True,
        "RegexUrl": ["/school/"],
        "sequence": sequences['linkedin']['COMPANY']
    },
    # PEOPLE
    {
        "website": "linkedin.com",
        "type": "peoples",
        "require_auth": True,
        "RegexUrl": ["/search/results/people"],
        "sequence": {
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
        "require_auth": True,
        "RegexUrl": ["/in/"],
        "sequence": sequences['linkedin']['PEOPLE']
    },
    # --- indeed.com ---
    {
        "website": "indeed.com",
        "type": "jobs",
        "require_auth": True,
        "RegexUrl": ["/jobs", "/emplois", ""],
        "sequence": {
            ":loop": {
                "pagination": 1,
                "listing": {
                    ":execute_script": 'document.querySelector("html").scroll(0, 9999999)',
                    ":get:all": {"property": "href", "selector": 'td.resultContent h2 > a'},
                    f":click_1": "#mosaic-modal-mosaic-provider-desktopserp-jobalert-popup > div > div > div.icl-Modal > div > button",
                    f":click_2": 'nav[role="navigation"] > div:last-child > a',
                },
            }
        }
    },
    {
        "website": "indeed.com",
        "type": "job",
        "require_auth": True,
        "RegexUrl": ["/viewjob", '/job/'],
        "sequence": {
            "JOB_TITLE:get": "h1 > span",
            "JOB_LOCATION:get": ".css-6z8o9s > div",
            "JOB_SPECIFICATION:get": "span.jobsearch-JobMetadataHeader-item",
            "JOB_REQUIREMENTS:get": "#qualificationsSection li > p",
            "JOB_TIME:get": "#mosaic-belowFullJobDescription + .css-q7fux ul li > *:last-child",
            "JOB_ADVANTAGE:get": "#benefits > div",
            "JOB_WORKTIME:get": "#jobDetailsSection > div:last-child > div:last-child",
            # COMPANY
            "COMPANY_LOCATION:get": ".css-6z8o9s > div",
            "COMPANY_PAGE:get": {
                "selector": ".jobsearch-CompanyInfoContainer a",
                "property": "href"
            },
            ":goto": '.jobsearch-CompanyInfoContainer a',
            ":sequence": sequences['indeed']['COMPANY'],
            # f":goto_{rand()}": ":original_url",
            # ":execute_script": "history.back();",
            # ":wait": 2,
        }
    },
    {
        "website": "indeed.com",
        "type": "company",
        "require_auth": True,
        "RegexUrl": ["/cmp/"],
        "sequence": {
            "COMPANY_NAME:get": 'header > h2',
            "COMPANY_RATE:get": 'li[data-tn-element="reviews-tab"] > a > div',
            "COMPANY_JOBS_COUNT:get": 'li[data-tn-element="jobs-tab-tab"] > a > div',
            "COMPANY_CREATION_DATE:get": 'li[data-testid="companyInfo-founded"] > div:last-child',
            "COMPANY_EMPLOYEES_COUNT:get": 'li[data-testid="companyInfo-employee"] > div:last-child',
            "COMPANY_REVENUE:get": 'li[data-testid="companyInfo-revenue"] > div:last-child',
            "COMPANY_SECTOR:get": 'li[data-testid="companyInfo-industry"] > div:last-child',
            "COMPANY_LOCATION:get": 'li[data-testid="companyInfo-headquartersLocation"] > div:last-child',
            # COMPANY EMAIL
            "COMPANY_WEBSITE:get": {
                "selector": 'li[data-testid="companyInfo-companyWebsite"] a',
                "property": "href"
            },
            # APPLICATION
            ":goto": 'li[data-tn-element="interviews-tab"] > a',
            "COMPANY_APPLICATION_EXPERIENCE:get": '[data-tn-component="summary-experience-card"] > div > div > div:last-child',
            "COMPANY_APPLICATION_DIFFICULTY:get": '[data-tn-component="summary-difficulty-card"] > div > div > div:last-child',
            "COMPANY_APPLICATION_TIME:get": '[data-tn-component="summary-hiring-duration-card"] > div > div > div:last-child',
            # ":execute_script": "history.back();",
            # ":wait": 2,
        }
    },
    # --- pole-emploi.com ---
    {
        "website": "pole-emploi.com",
        "type": "jobs",
        "require_auth": True,
        "RegexUrl": ["/offres/recherche"],
        "sequence": {
            ":loop": {
                "pagination": 1,
                "listing": {
                    ":execute_script_1": 'document.querySelector("html").scroll(0, 9999999)',
                    ":click_1": "#zoneAfficherPlus a",
                    ":execute_script_2": 'document.querySelector("html").scroll(0, 9999999)',
                    ":click_2": "#zoneAfficherPlus a",
                    ":execute_script_3": 'document.querySelector("html").scroll(0, 9999999)',
                    ":click_3": "#zoneAfficherPlus a",
                    ":get:all": {"property": "href", "selector": 'li.result > a.media'}
                },
            }
        }
    },
    {
        "website": "pole-emploi.com",
        "type": "job",
        "require_auth": True,
        "RegexUrl": ["/offres/recherche/detail/"],
        "sequence": {
            "JOB_NAME:get": "#labelPopinDetailsOffre > span:last-child",
            "JOB_LOCATION:get": 'p[itemprop="jobLocation"] span[itemprop="name"]',
            "JOB_TIME:get": 'span[itemprop="datePosted"]',
            "JOB_SPECIFICATION:get": 'div.description-aside dd',
            "JOB_WORTIME:get": 'div.description-aside dd[itemprop="workHours"]',
            "JOB_REVENUE:get": 'div.description-aside [itemprop="baseSalary"] + ul li',
            # "JOB_EXPERIENCE:get": "",
            # "JOB_REQUIREMENTS:get": "",
            # "JOB_SKILLS:get": "",
            # "JOB_INFOS": "",
            "COMPANY_NAME:get": '[itemprop="hiringOrganization"] + h2 + .media .media-body h3',
            "COMPANY_PHONE:get": '[itemprop="hiringOrganization"] + h2 + .media [itemprop="telephone"]',
            "COMPANY_WEBSITE:get": '[itemprop="hiringOrganization"] + h2 + .media .media-body dl a',
            ":click": '[itemprop="hiringOrganization"] + h2 + .media .media-body p > a',
            ":sequence": None,
        }
    },
    {
        "website": "pole-emploi.com",
        "type": "company",
        "require_auth": True,
        "RegexUrl": ["/page-entreprise"],
        "sequence": {
            "COMPANY_NAME:get": "h1",
            "COMPANY_TITLE:get": "h1 + p",
            "COMPANY_EMPLOYEES_COUNT": ".bloc-illustration > div span > p:last-child",
            "COMPANY_SECTOR": ".bloc-illustration > div:last-child span > p:last-child",
            "COMPANY_EMAIL": ".vcard-entreprise .vcard-descriptif > p:last-child",
            "COMPANY_WEBSITE": ".vcard-entreprise .vcard-descriptif > p:last-child a",
            "COMPANY_FACEBOOK": "",
            "COMPANY_TWITTER": "",
            "COMPANY_LINKEDIN": "",
        }
    }
]


def find_model(url=None, models=None):
    if models is None:
        models = all_models
    if url is None:
        return
    print(Fore.WHITE + 'find_model()')
    for model in models:
        if model['website'] in url:
            for regex in model['RegexUrl']:
                if regex in url:
                    print(Fore.GREEN + 'model founded')
                    print(Style.RESET_ALL)
                    return model
                else:
                    pass
        else:
            pass
    print(url)
    print(Fore.RED + 'Aucun modèle')
    print(Style.RESET_ALL)
    return {
        "message": 'No model found',
        "sequence": {}
    }
