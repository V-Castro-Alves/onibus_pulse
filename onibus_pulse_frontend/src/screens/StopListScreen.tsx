import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, AlertCircle, Circle } from 'lucide-react';
import './StopListScreen.css';

interface Stop {
  stop_id: string;
  stop_name: string;
  stop_order: number;
}

const StopListScreen: React.FC = () => {
  const { routeId, shapeId } = useParams<{ routeId: string; shapeId: string }>();
  const navigate = useNavigate();
  const [stops, setStops] = useState<Stop[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStops = async () => {
      try {
        const response = await fetch(`http://localhost:8000/stops/${shapeId}`);
        if (!response.ok) throw new Error('Failed to fetch stops');
        const data = await response.json();
        // Sort stops by order just in case
        setStops(data.sort((a: Stop, b: Stop) => a.stop_order - b.stop_order));
        setError(null);
      } catch (err) {
        setError('Could not load stops for this direction.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (shapeId) fetchStops();
  }, [shapeId]);

  return (
    <div className="stop-list-screen">
      <div className="screen-header">
        <h2 className="screen-title">Select Stop</h2>
        <p className="screen-subtitle">Route {routeId}</p>
      </div>

      <div className="stops-timeline">
        {loading && (
          <div className="state-message">
            <Loader2 className="animate-spin" size={32} />
            <p>Loading stops...</p>
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

        {!loading && !error && stops.map((stop) => (
          <div 
            key={stop.stop_id} 
            className="stop-item"
            onClick={() => navigate(`/eta/${routeId}/${shapeId}/${stop.stop_id}`)}
          >
            <div className="stop-indicator">
              <div className="timeline-line"></div>
              <Circle className="stop-dot" size={16} fill="white" />
            </div>
            <div className="stop-content">
              <span className="stop-name">{stop.stop_name}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StopListScreen;
