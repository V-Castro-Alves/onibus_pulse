import React, { useState, useEffect } from 'react';
import { Search, Loader2, AlertCircle } from 'lucide-react';
import RouteCard from '../components/RouteCard';
import './HomeScreen.css';

interface RouteItem {
  route_id: string;
  route_long_name: string;
}

const HomeScreen: React.FC = () => {
  const [routes, setRoutes] = useState<RouteItem[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        // Backend URL should be configurable, defaulting to localhost:8000
        const response = await fetch('http://localhost:8000/routes/list');
        if (!response.ok) throw new Error('Failed to fetch routes');
        const data = await response.json();
        setRoutes(data);
        setError(null);
      } catch (err) {
        setError('Could not load bus routes. Please check if the backend is running.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRoutes();
  }, []);

  const filteredRoutes = routes.filter(route => 
    route.route_id.toLowerCase().includes(search.toLowerCase()) ||
    route.route_long_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="home-screen">
      <div className="search-container">
        <Search className="search-icon" size={20} />
        <input 
          type="text" 
          placeholder="Search line number or name..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
      </div>

      <div className="routes-list">
        {loading && (
          <div className="state-message">
            <Loader2 className="animate-spin" size={32} />
            <p>Loading routes...</p>
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

        {!loading && !error && filteredRoutes.length === 0 && (
          <div className="state-message">
            <p>No routes found matching "{search}"</p>
          </div>
        )}

        {!loading && !error && filteredRoutes.map(route => (
          <RouteCard 
            key={route.route_id} 
            routeId={route.route_id} 
            routeName={route.route_long_name} 
          />
        ))}
      </div>
    </div>
  );
};

export default HomeScreen;
