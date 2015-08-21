'''
Created on Jul 24, 2015

@author: tguo
'''
def parse_yahoo_historical(fh, adjusted=True, asobject=False):  
    """  
    Parse the historical data in file handle fh from yahoo finance.  
  
    *adjusted*  
      If True (default) replace open, close, high, and low prices with  
      their adjusted values. The adjustment is by a scale factor, S =  
      adjusted_close/close. Adjusted prices are actual prices  
      multiplied by S.  
  
      Volume is not adjusted as it is already backward split adjusted  
      by Yahoo. If you want to compute dollars traded, multiply volume  
      by the adjusted close, regardless of whether you choose adjusted  
      = True|False.  
  
  
    *asobject*  
      If False (default for compatibility with earlier versions)  
      return a list of tuples containing  
  
        d, open, close, high, low, volume  
  
      If None (preferred alternative to False), return  
      a 2-D ndarray corresponding to the list of tuples.  
  
      Otherwise return a numpy recarray with  
  
        date, year, month, day, d, open, close, high, low,  
        volume, adjusted_close  
  
      where d is a floating poing representation of date,  
      as returned by date2num, and date is a python standard  
      library datetime.date instance.  
  
      The name of this kwarg is a historical artifact.  Formerly,  
      True returned a cbook Bunch  
      holding 1-D ndarrays.  The behavior of a numpy recarray is  
      very similar to the Bunch.  
  
    """  
  
    lines = fh.readlines()  
  
    results = []  
  
    datefmt = '%Y-%m-%d'  
  
    for line in lines[1:]:  
  
        vals = line.split(',')  
        if len(vals)!=7:  
            continue      # add warning?  
        datestr = vals[0]  
        #dt = datetime.date(*time.strptime(datestr, datefmt)[:3])  
        # Using strptime doubles the runtime. With the present  
        # format, we don't need it.  
        dt = datetime.date(*[int(val) for val in datestr.split('-')])  
        dnum = date2num(dt)  
        open, high, low, close =  [float(val) for val in vals[1:5]]  
        volume = float(vals[5])  
        aclose = float(vals[6])  
  
        results.append((dt, dt.year, dt.month, dt.day,  
                        dnum, open, close, high, low, volume, aclose))  
    results.reverse()  
    d = np.array(results, dtype=stock_dt)  
    if adjusted:  
        scale = d['aclose'] / d['close']  
        scale[np.isinf(scale)] = np.nan  
        d['open'] *= scale  
        d['close'] *= scale  
        d['high'] *= scale  
        d['low'] *= scale  
  
    if not asobject:  
        # 2-D sequence; formerly list of tuples, now ndarray  
        ret = np.zeros((len(d), 6), dtype=np.float)  
        ret[:,0] = d['d']  
        ret[:,1] = d['open']  
        ret[:,2] = d['close']  
        ret[:,3] = d['high']  
        ret[:,4] = d['low']  
        ret[:,5] = d['volume']  
        if asobject is None:  
            return ret  
        return [tuple(row) for row in ret]  
  
    return d.view(np.recarray)  # Close enough to former Bunch return  