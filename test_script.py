from datetime import time



'''for _, rows in all_talents.iterrows():
        tid = rows['talent_id']
        role = rows['role']
        dates = rows['date']
        shifts = rows['shifts']
        if tid not in results:
            results[tid] = {
                "role": role,
                "availability": {}
            }
        for date in dates:
            if date not in results[tid]['availability']:
                results[tid]['availability'][date] = []
            for shift in shifts:
                if shift not in results[tid]['availability'][date]:
                    results[tid]['availability'][date].append(shift)'''


'''results = {
        date:{
            shift: {'roles': grp.set_index('role')['count'].to_dict(),
             'start' : grp['start'].iloc[0],
             'end' : grp['end'].iloc[0]}
        for shift, grp in group.groupby('shift')
        }for date, group in week_shifts.groupby('date')
    }'''  