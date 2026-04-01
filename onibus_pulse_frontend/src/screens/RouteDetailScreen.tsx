import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, AlertCircle, MapPin, ArrowRight } from 'lucide-react';
import './RouteDetailScreen.css';

interface Trip {
  trip_headsign: string;
  shape_id: string;
  direction_id: number;
}

const RouteDetailScreen: React.FC = () => {
  const { routeId } = useParams<{ routeId: string }>();
  const navigate = useNavigate();
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const response = await fetch(`http://localhost:8000/routes/${routeId}`);
        if (!response.ok) throw new Error('Failed to fetch route directions');
        const data = await response.json();
        setTrips(data);
        setError(null);
      } catch (err) {
        setError('Could not load directions for this route.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (routeId) fetchTrips();
  }, [routeId]);

  return (
    <div className="route-detail-screen">
      <div className="screen-header">
        <h2 className="screen-title">Select Direction</h2>
        <p className="screen-subtitle">Line {routeId}</p>
      </div>

      <div className="trips-list">
        {loading && (
          <div className="state-message">
            <Loader2 className="animate-spin" size={32} />
            <p>Loading directions...</p>
          </div>
        )}

        {error && (
          <div className="state-message error">
            <AlertCircle size={32} />
            <p>{error}</p>
            <button onClick={() => window.location.reload()} className="retry-button">
              Retry
            </button>
          </div>
        )}

        {!loading && !error && trips.length === 0 && (
          <div className="state-message">
            <p>No directions found for this route.</p>
          </div>
        )}

        {!loading && !error && trips.map((trip, index) => (
          <div 
            key={`${trip.shape_id}-${index}`} 
            className="trip-card"
            onClick={() => navigate(`/route/${routeId}/shape/${trip.shape_id}`)}
          >
            <div className="trip-icon">
              <MapPin size={20} />
            </div>
            <div className="trip-info">
              <span className="trip-label">To</span>
              <span className="trip-headsign">{trip.trip_headsign}</span>
            </div>
            <div className="trip-action">
              <ArrowRight size={20} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RouteDetailScreen;
