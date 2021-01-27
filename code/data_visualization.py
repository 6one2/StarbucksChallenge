import matplotlib.pyplot as plt
from matplotlib.patches import Patch


color_evt = {
    'offer received':'red',
    'offer viewed':'blue',
    'transaction':'black',
    'offer completed':'yellow'
}

legend_elements = [
    Patch(facecolor='red', label='offer received'),
    Patch(facecolor='blue', label='offer viewed'),
    Patch(facecolor='black', label='transaction'),
    Patch(facecolor='yellow', label='offer completed')
]

def time_line(event, transactions=[], legend=False, xlabel=True, text=''):
    ax = plt.gca()
    ax.yaxis.set_visible(False)
    ymax = 1
    tag = 'VIEWED' if event.viewed > 0 else 'not viewed'
    Text = text + event.details['offer_type'] + ' / ' +tag
    Text_code = text + event.details['code'] + ' / ' +tag
    evt_list = event.events['event'].tolist()
    color_list = [color_evt[k] for k in evt_list]
    
    evt_id = event.events['offer_id'].tolist()
    style_list = ['solid' if x == event.offer_id else 'dashed' for x in evt_id]
    
    
    if len(transactions) > 0:
        ymax = transactions.amount.max()+5
        ax.plot(transactions.time, transactions.amount, 'ko', mfc='white', ms=10)
        ax.yaxis.set_visible(True)
        ax.set_ylabel('transaction $')
        
    ax.vlines(
        x=event.events['time'],
        ymax=ymax, 
        ymin=0, 
        color=color_list,
        ls=style_list,
        lw=3
    )
    ax.fill_between(x=[event.start,event.end], y1=[0,0], y2=[ymax,ymax], alpha=.2)
    ax.text(
        0.01,0.8,
        Text, 
        weight='bold', 
        ha='left',
        transform=ax.transAxes
    )
    if xlabel:
        ax.set_xlabel('time (hours)')
    
    if legend:
        ax.legend(handles=legend_elements, loc='best')
    
    plt.grid(False, axis='y')
    