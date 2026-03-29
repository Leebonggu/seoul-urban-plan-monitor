"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Center } from "@/lib/types";
import { GRADE_COLORS } from "@/lib/centers";

const LABEL_STYLE = `
  .center-label {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 11px !important;
    font-weight: 600;
    color: #374151;
    text-shadow: 1px 1px 2px white, -1px -1px 2px white, 1px -1px 2px white, -1px 1px 2px white;
    white-space: nowrap;
  }
  .center-label::before {
    display: none !important;
  }
`;

function FitBounds() {
  const map = useMap();
  useEffect(() => {
    map.setView([37.5665, 126.978], 11);
  }, [map]);
  return null;
}

interface Props {
  centers: Center[];
  onCenterClick?: (name: string) => void;
}

export default function CenterMap({ centers, onCenterClick }: Props) {
  return (
    <MapContainer
      center={[37.5665, 126.978]}
      zoom={11}
      className="h-full w-full rounded-xl"
      style={{ minHeight: "400px", zIndex: 0 }}
    >
      <style dangerouslySetInnerHTML={{ __html: LABEL_STYLE }} />
      <FitBounds />
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
      {centers.map((c) => {
        const color = GRADE_COLORS[c.grade] || "#999";
        const radius = Math.max(8, Math.min(28, c.count * 1.5));
        return (
          <CircleMarker
            key={c.name}
            center={[c.lat, c.lng]}
            radius={radius}
            pathOptions={{
              color,
              fillColor: color,
              fillOpacity: 0.7,
              weight: 2,
            }}
            eventHandlers={{
              click: () => onCenterClick?.(c.name),
            }}
          >
            <Tooltip direction="top" offset={[0, -10]} permanent className="center-label">
              {c.name}
            </Tooltip>
            <Popup>
              <div className="text-sm">
                <p className="font-bold">{c.name}</p>
                <p>등급: {c.grade}</p>
                <p>고시문: {c.count}건</p>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
