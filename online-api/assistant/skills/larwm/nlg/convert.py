#!/usr/bin/env python3
# -*- coding: utf-8 -*-
HOUR_LOOKUP = {
    'un':1,
    'dau':2,
    'ddau':2,
    'tri':3,
    'dri':3,
    'pedwar':4,
    'bedwar':4,
    'pump':5,
    'bump':5,
    'chwech':6,
    'saith':7,
    'wyth':8,
    'naw':9,
    'deg':10,
    'ddeg':10,
    'un ar ddeg':11
}


MINUTES_LOOKUP={
    'pum':5,
    'deg':10,
    'ugain':20,
}


HANNER_CHWARTER_LOOKUP={
    'chwarter':15,
    'hanner':30
}    

HANNER_NOS_DYDD_LOOKUP={
    'hanner nos':0,
    'canol nos':0,
    'ganol nos':0,
    'hanner dydd':12,
    'ganol dydd':12,
    'canol dydd':12
}  

def convertTo24hr(hour, day_period_string):
    if day_period_string=='yn y prynhawn' or day_period_string=="gyda'r nos":
        hour+=12
    return hour 


def convertHannerChwarter(hanner_chwarter_string, i_wedi_string):
    minutes=HANNER_CHWARTER_LOOKUP[hanner_chwarter_string]
    if minutes==15:
        if i_wedi_string=='i':
            minutes = minutes+30
    return minutes

