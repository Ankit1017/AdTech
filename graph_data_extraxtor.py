from database_cls import *
from collections import defaultdict
from datetime import datetime,timedelta

def cf(user,cat,ad_runs_data,ad_runs_data1,ad_runs_data2,views_by_date,datasets,name=""):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    start_date1 = end_date - timedelta(days=30)
    start_date2 = end_date - timedelta(days=365)
    if name!="":
        logsWek = Log.query.filter(Log.time_shown >= start_date, 
                            Log.time_shown <= end_date, 
                            Log.category_name == cat, 
                            Log.company_name == user,
                            Log.ad_name ==name).all()
        logsMon = Log.query.filter(Log.time_shown >= start_date1, 
                            Log.time_shown <= end_date, 
                            Log.category_name == cat, 
                            Log.company_name == user,
                            Log.ad_name ==name).all()
        logsYer = Log.query.filter(Log.time_shown >= start_date2, 
                            Log.time_shown <= end_date, 
                            Log.category_name == cat, 
                            Log.company_name == user,
                            Log.ad_name ==name).all()
        logs = Log.query.filter(Log.category_name == cat, 
                        Log.company_name == user,
                        Log.ad_name ==name).all()
    else:
        logsWek = Log.query.filter(Log.time_shown >= start_date, 
                            Log.time_shown <= end_date, 
                            Log.category_name == cat, 
                            Log.company_name == user).all()
        logsMon = Log.query.filter(Log.time_shown >= start_date1, 
                            Log.time_shown <= end_date, 
                            Log.category_name == cat, 
                            Log.company_name == user).all()
        logsYer = Log.query.filter(Log.time_shown >= start_date2, 
                            Log.time_shown <= end_date, 
                            Log.category_name == cat, 
                            Log.company_name == user).all()
        logs = Log.query.filter(Log.category_name == cat, 
                        Log.company_name == user).all()
    for log in logsWek:
        date_key = log.time_shown.strftime('%Y-%m-%d')  # Format date as 'YYYY-MM-DD'
        views_by_date[date_key] += 1
    for log in logsWek:
        week_start = log.time_shown - timedelta(days=log.time_shown.weekday())
        week_end = week_start + timedelta(days=6)
        week_key = f"{week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}"

        if log.ad_name not in ad_runs_data:
            ad_runs_data[log.ad_name] = {}

        if week_key not in ad_runs_data[log.ad_name]:
            ad_runs_data[log.ad_name][week_key] = 0

        ad_runs_data[log.ad_name][week_key] += 1
    for log in logsMon:
        week_start = log.time_shown - timedelta(days=log.time_shown.weekday())
        week_end = week_start + timedelta(days=29)
        week_key = f"{week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}"

        if log.ad_name not in ad_runs_data1:
            ad_runs_data1[log.ad_name] = {}

        if week_key not in ad_runs_data1[log.ad_name]:
            ad_runs_data1[log.ad_name][week_key] = 0

        ad_runs_data1[log.ad_name][week_key] += 1
    for log in logsYer:
        week_start = log.time_shown - timedelta(days=log.time_shown.weekday())
        week_end = week_start + timedelta(days=364)
        week_key = f"{week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}"

        if log.ad_name not in ad_runs_data2:
            ad_runs_data2[log.ad_name] = {}

        if week_key not in ad_runs_data2[log.ad_name]:
            ad_runs_data2[log.ad_name][week_key] = 0

        ad_runs_data2[log.ad_name][week_key] += 1
    ad_views = defaultdict(list)
    for log in logs:
        ad_views[log.ad_name].append(log.time_shown.weekday())

    # Calculate views for each ad on each weekday
    ad_views_weekdays = {}
    for ad_name, weekdays in ad_views.items():
        views_per_day = [weekdays.count(i) for i in range(7)]
        ad_views_weekdays[ad_name] = views_per_day

    # Format the data into the desired structure
    colors = ['rgb(4, 169, 245)', 'rgb(29, 233, 182)', 'rgb(163, 137, 212)']  # Add more colors if needed
    for i, (ad_name, views_per_day) in enumerate(ad_views_weekdays.items()):
        dataset = {
            'label': f'Dataset {i+1}',
            'backgroundColor': colors[i % len(colors)],
            'data': views_per_day
        }
        datasets.append(dataset)
    k=0
    for ad_name, weekdays in ad_views.items():
        datasets[k]['label']=ad_name
        k+=1