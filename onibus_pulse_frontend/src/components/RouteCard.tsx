import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Bus } from 'lucide-react';
import './RouteCard.css';

interface RouteCardProps {
  routeId: string;
  routeName: string;
}

const RouteCard: React.FC<RouteCardProps> = ({ routeId, routeName }) => {
  const navigate = useNavigate();

  return (
    <div className="route-card" onClick={() => navigate(`/route/${routeId}`)}>
      <div className="route-icon">
        <Bus size={20} />
      </div>
      <div className="route-info">
        <span className="route-id">{routeId}</span>
        <span className="route-name">{routeName}</span>
      </div>
      <div className="route-action">
        <ArrowRight size={20} />
      </div>
    </div>
  );
};

export default RouteCard;
