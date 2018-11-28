# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import pytest

from scoap3.modules.analysis.tasks import (get_authors_max_affiliation,
                                           authors_max_affiliations)

country_list = {
    "Denmark": 46336.86975,
    "Australia": 44571.0954,
    "CERN": 3000000.0,
    "Germany": 44830.53407,
    "USA": 53812.40265,
    "France": 38334.15531,
    "South Korea": 35479.39286,
    "DESY": 1899999.0,
    "SLACK": 1899997.0,
    "FERMILAB": 1899998.0,
    "Switzerland": 57415.85718,
    "Japan": 38642.364,
    "Poland": 26626.14139,
    "KEK": 1899996.0,
    "JINR": 1900000.0,
    "Russia": 24591.28876
}

testauthors = [
    ({
        "full_name": "Someone One",
        "affiliations": [
            {
             "country": "Denmark",
             "value": "CP3-Origins, University of Southern Denmark, Campusvej 55, Odense M, 5230, Denmark"
            }
        ]
    }, "Denmark"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {
                "country": "Australia",
                "value": "ARC Center of Excellence for Particle Physics at the Terascale, University of Adelaide, Adelaide, South Australia, 5005, Australia"
            }
        ]
    }, "Australia"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "Germany", "value": u"PRISMA Cluster of Excellence, Johannes Gutenberg-Universität Mainz, Staudingerweg 9, Mainz, 55128, Germany"},
            {"country": "CERN", "value": "Theoretical Physics Department, CERN, Geneva, 1211, Switzerland"}
        ]
    }, "CERN"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "Germany", "value": u"PRISMA Cluster of Excellence, Johannes Gutenberg-Universität Mainz, Staudingerweg 9, Mainz, 55128, Germany"}
        ]
    }, "Germany"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "France", "value": u"Institut de Physique Théorique, Paris Saclay, CEA, CNRS, Gif-sur-Yvette, 91191, France"},
            {"country": "USA", "value": "Physics Department, University of Southern California, 920 Bloom Walk, Los Angeles, CA, 90089, U.S.A."}
        ]
    }, "USA"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "France", "value": u"Laboratoire de Physique Théorique, Département de Physique de l’ENS, École Normale Supérieure, Sorbonne Université, CNRS, PSL Research University, Paris, 75005, France"},
            {"country": "France", "value": u"Sorbonne Université, École Normale Supérieure, CNRS, Laboratoire de Physique Théorique (LPT ENS), Paris, 75005, France"},
            {"country": "France", "value": u"Institut de Physique Théorique, Paris Saclay, CEA, CNRS, Gif-sur-Yvette, 91191, France"}
        ]
    }, "France"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "South Korea", "value": "School of Physics, Korea Institute for Advanced Study, 85 Hoegiro, Dongdaemun-gu, Seoul, 130-722, Republic of Korea"}
        ]
    }, "South Korea"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "Germany", "value": u"Physikalisches Institut, Universität Bonn, Bonn, Germany"},
            {"country": "CERN", "value": "CERN, Geneva, Switzerland"}
        ]
    }, "CERN"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "France", "value": "CNRS, France"},
            {"country": "DESY", "value": "DESY, Germany"}
        ]
    }, "DESY"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "USA", "value": "USA"},
            {"country": "SLACK", "value": "SLACK, USA"}
        ]
    }, "SLACK"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "Japan", "value": "Japan"},
            {"country": "KEK", "value": "KEK, Japan"},
            {"country": "FERMILAB", "value": "FERMILAB, USA"}
        ]
    }, "FERMILAB"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "Poland", "value": "Poland"},
            {"country": "FERMILAB", "value": "Fermilab, USA"},
            {"country": "SLACK", "value": "SLAK, USA"}
        ]
    }, "FERMILAB"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "CERN", "value": "CERN"},
            {"country": "JINR", "value": "JINR"}
        ]
    }, "CERN"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "JINR", "value": "JINR"},
            {"country": "DESY", "value": "DESY, Germany"},
            {"country": "Russia", "value": "Russia"}
        ]
    }, "JINR"),
    ({
        "full_name": "Someone One",
        "affiliations": [
            {"country": "CERN", "value": "CERN"},
            {"country": "DESY", "value": "DESY, Germany"},
            {"country": "KEK", "value": "KEK, Japan"},
            {"country": "FERMILAB", "value": "Fermilab, USA"}
        ]
    }, "CERN")
]

testarticles = [
    ({
        "_source": {
            "authors": [
                {
                    "full_name": "Someone One",
                    "affiliations": [
                        {"country": "CERN", "value": "CERN"},
                        {"country": "DESY", "value": "DESY, Germany"},
                        {"country": "KEK", "value": "KEK, Japan"},
                        {"country": "FERMILAB", "value": "Fermilab, USA"}
                    ]
                },
                {
                    "full_name": "Someone Two",
                    "affiliations": [
                        {"country": "Poland", "value": "Poland"},
                        {"country": "FERMILAB", "value": "Fermilab, USA"},
                        {"country": "SLACK", "value": "SLAK, USA"}
                    ]
                },
                {
                    "full_name": "Someone Three",
                    "affiliations": [
                        {"country": "France", "value": u"Laboratoire de Physique Théorique, Département de Physique de l’ENS, École Normale Supérieure, Sorbonne Université, CNRS, PSL Research University, Paris, 75005, France"},
                        {"country": "France", "value": u"Sorbonne Université, École Normale Supérieure, CNRS, Laboratoire de Physique Théorique (LPT ENS), Paris, 75005, France"},
                        {"country": "France", "value": u"Institut de Physique Théorique, Paris Saclay, CEA, CNRS, Gif-sur-Yvette, 91191, France"}
                    ]
                },
                {
                    "full_name": "Someone Four",
                    "affiliations": [
                        {"country": "CERN", "value": "CERN"},
                        {"country": "JINR", "value": "JINR"}
                    ]
                }
            ]
        }
    },
    {
        "CERN": 2,
        "Fermilab": 1,
        "France": 1
    },
    {
        'countries_ordering': 'value1',
        'authors': {
            "Someone One": {"affiliation": "CERN", "country": "CERN"},
            "Someone Two": {"affiliation": "Fermilab", "country": "Fermilab, USA"},
            "Someone Three": {"affiliation": "France", "country": u"Laboratoire de Physique Théorique, Département de Physique de l’ENS, École Normale Supérieure, Sorbonne Université, CNRS, PSL Research University, Paris, 75005, France"},
            "Someone Four": {"affiliation": "CERN", "country": "CERN"},
        }
    }
    )
]


@pytest.mark.parametrize("author,expected", testauthors)
def test_get_author_max_affiliation(author, expected):
    max_aff = get_authors_max_affiliation(author, country_list)
    assert max_aff['country'] == expected


@pytest.mark.parametrize("article,expected_result,expected_details", testarticles)
def test_authors_max_affiliations(article, expected_result, expected_details):
    result, details = authors_max_affiliations(article, country_list, "value1")
    assert result == expected_result
    assert details == expected_details
