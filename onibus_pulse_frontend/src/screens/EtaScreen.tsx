import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Loader2, AlertCircle, Clock, RefreshCcw, Wifi } from 'lucide-react';
import './EtaScreen.css';

interface ETAInfo {
  vehicle_prefix: string;
  scheduled_arrival: string;
  delay_seconds: number;
  eta_time: string;
  remaining_minutes: number;
  status: string;
}

const EtaScreen: React.FC = () => {
  const { routeId, shapeId, stopId } = useParams<{ 
    routeId: string; 
    shapeId: string; 
    stopId: string; 
  }>();
  
  const [etas, setEtas] = useState<ETAInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  const fetchETAs = async (isAutoRefresh = false) => {
    if (!isAutoRefresh) setLoading(true);
    else setRefreshing(true);

    try {
      const response = await fetch(`http://localhost:8000/eta/${routeId}/${shapeId}/${stopId}`);
      if (!response.ok) throw new Error('Failed to fetch ETA');
      const data = await response.json();
      setEtas(data);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      if (!isAutoRefresh) setError('Could not load arrival times.');
      console.error(err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchETAs();

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      fetchETAs(true);
    }, 30000);

    return () => clearInterval(interval);
  }, [routeId, shapeId, stopId]);

  return (
    <div className="eta-screen">
      <div className="screen-header-with-action">
        <div className="screen-header">
          <h2 className="screen-title">Live Arrivals</h2>
          <p className="screen-subtitle">
            Updated at {lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
          </p>
        </div>
        <button 
          className={`refresh-button ${refreshing ? 'spinning' : ''}`} 
          onClick={() => fetchETAs(true)}
          disabled={loading || refreshing}
          title="Manual refresh"
        >
          <RefreshCcw size={20} />
        </button>
      </div>

      <div className="eta-list">
        {loading && (
          <div className="state-message">
            <Loader2 className="animate-spin" size={32} />
            <p>Fetching live data...</p>
          </div>
        )}

        {error && (
          <div className="state-message error">
            <AlertCircle size={32} />
            <p>{error}</p>
            <button onClick={() => fetchETAs()} className="retry-button">
              Retry
            </button>
          </div>
        )}

        {!loading && !error && etas.length === 0 && (
          <div className="state-message">
            <Wifi size={32} className="offline-icon" />
            <p>No active vehicles found for this route right now.</p>
            <p className="small-text">Buses might be out of service or real-time data is unavailable.</p>
          </div>
        )}

        {!loading && !error && etas.map((eta, index) => (
          <div key={`${eta.vehicle_prefix}-${index}`} className="eta-card">
            <div className="eta-main">
              <div className="vehicle-info">
                <span className="vehicle-label">Vehicle</span>
                <span className="vehicle-id">#{eta.vehicle_prefix}</span>
              </div>
              <div className="arrival-countdown">
                <span className="minutes">{eta.remaining_minutes}</span>
                <span className="minutes-label">min</span>
              </div>
            </div>
            
            <div className="eta-details">
              <div className="detail-item">
                <Clock size={14} />
                <span>Scheduled: {eta.scheduled_arrival}</span>
              </div>
              <div className={`status-badge ${eta.delay_seconds > 60 ? 'delayed' : 'on-time'}`}>
                {eta.delay_seconds > 60 
                  ? `${Math.floor(eta.delay_seconds / 60)}m delay` 
                  : 'On time'
                }
              </div>
            </div>
            
            <div className="live-indicator">
              <div className="pulse-dot mini"></div>
              <span>Live tracking active</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EtaScreen;
