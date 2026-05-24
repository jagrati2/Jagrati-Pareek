// CountryExplorer.jsx
// Project 2 — Fetch from a public API + search/filter + loading & error states
// New concepts: useEffect, fetch(), lifting state up, conditional rendering

import { useState, useEffect } from "react";

const API = "https://restcountries.com/v3.1/all?fields=name,flags,population,region,capital,subregion";

const REGIONS = ["All", "Africa", "Americas", "Asia", "Europe", "Oceania"];

// --- SMALL COMPONENTS ---

// Shows while data is loading
function LoadingState() {
  return (
    <div style={{ textAlign: "center", padding: "3rem 1rem", color: "var(--color-text-secondary)" }}>
      <div style={{ fontSize: 32, marginBottom: 12 }}>🌍</div>
      <p style={{ margin: 0, fontSize: 14 }}>Fetching countries...</p>
    </div>
  );
}

// Shows when the fetch fails
function ErrorState({ message, onRetry }) {
  return (
    <div style={{
      textAlign: "center", padding: "3rem 1rem",
      background: "var(--color-background-danger)",
      borderRadius: 12, border: "0.5px solid var(--color-border-danger)",
      margin: "1rem 0"
    }}>
      <div style={{ fontSize: 28, marginBottom: 8 }}>⚠️</div>
      <p style={{ margin: "0 0 4px", fontWeight: 500, fontSize: 14, color: "var(--color-text-danger)" }}>
        Something went wrong
      </p>
      <p style={{ margin: "0 0 16px", fontSize: 12, color: "var(--color-text-secondary)" }}>{message}</p>
      <button onClick={onRetry} style={{ fontSize: 13 }}>Try again</button>
    </div>
  );
}

// Shows when search returns nothing
function EmptyState({ query, region }) {
  return (
    <div style={{ textAlign: "center", padding: "3rem 1rem", color: "var(--color-text-secondary)" }}>
      <div style={{ fontSize: 32, marginBottom: 12 }}>🔍</div>
      <p style={{ margin: "0 0 4px", fontWeight: 500, fontSize: 14, color: "var(--color-text-primary)" }}>
        No countries found
      </p>
      <p style={{ margin: 0, fontSize: 12 }}>
        {query && `No results for "${query}"`}
        {query && region !== "All" && " in "}
        {region !== "All" && region}
      </p>
    </div>
  );
}

// Formats big numbers — 1000000 → 1,000,000
function formatPop(n) {
  return n.toLocaleString();
}

// A single country card
function CountryCard({ country }) {
  const capital = country.capital?.[0] ?? "N/A";

  return (
    <div style={{
      background: "var(--color-background-primary)",
      border: "0.5px solid var(--color-border-tertiary)",
      borderRadius: 14,
      overflow: "hidden",
      display: "flex",
      flexDirection: "column",
      transition: "transform 0.15s, border-color 0.15s",
    }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = "translateY(-3px)";
        e.currentTarget.style.borderColor = "var(--color-border-secondary)";
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.borderColor = "var(--color-border-tertiary)";
      }}
    >
      {/* Flag */}
      <img
        src={country.flags.svg}
        alt={`Flag of ${country.name.common}`}
        style={{ width: "100%", height: 120, objectFit: "cover", display: "block" }}
      />

      {/* Info */}
      <div style={{ padding: "14px 16px", flex: 1, display: "flex", flexDirection: "column", gap: 6 }}>
        <p style={{ margin: 0, fontWeight: 500, fontSize: 14, color: "var(--color-text-primary)" }}>
          {country.name.common}
        </p>

        <div style={{ display: "flex", flexDirection: "column", gap: 3, marginTop: 2 }}>
          <Row label="Capital" value={capital} />
          <Row label="Region" value={country.region} />
          <Row label="Population" value={formatPop(country.population)} />
        </div>
      </div>
    </div>
  );
}

// Label + value row inside a card
function Row({ label, value }) {
  return (
    <p style={{ margin: 0, fontSize: 12, color: "var(--color-text-secondary)" }}>
      <span style={{ color: "var(--color-text-primary)", fontWeight: 500 }}>{label}: </span>
      {value}
    </p>
  );
}

// Search input component
function SearchBox({ value, onChange }) {
  return (
    <div style={{ position: "relative", flex: 1 }}>
      <span style={{
        position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)",
        color: "var(--color-text-secondary)", fontSize: 16, pointerEvents: "none"
      }}>🔍</span>
      <input
        type="text"
        placeholder="Search for a country..."
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{ width: "100%", paddingLeft: 34, fontSize: 13 }}
      />
    </div>
  );
}

// Region filter buttons
// State lives in the PARENT (CountryExplorer) — this is "lifting state up"
function RegionFilter({ selected, onChange }) {
  return (
    <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
      {REGIONS.map(r => (
        <button
          key={r}
          onClick={() => onChange(r)}
          style={{
            fontSize: 12,
            padding: "5px 12px",
            background: selected === r ? "var(--color-background-info)" : "transparent",
            color: selected === r ? "var(--color-text-info)" : "var(--color-text-secondary)",
            border: selected === r
              ? "0.5px solid var(--color-border-info)"
              : "0.5px solid var(--color-border-tertiary)",
          }}
        >
          {r}
        </button>
      ))}
    </div>
  );
}

// --- MAIN COMPONENT ---
export default function CountryExplorer() {
  // State — I learned: group related state together
  const [countries, setCountries] = useState([]);   // all countries from API
  const [loading, setLoading] = useState(true);     // are we fetching right now?
  const [error, setError] = useState(null);         // did something go wrong?
  const [search, setSearch] = useState("");         // what the user typed
  const [region, setRegion] = useState("All");      // which region is selected

  // useEffect runs AFTER the component renders
  // The empty [] means "only run this once, when the app first loads"
  const fetchCountries = () => {
    setLoading(true);
    setError(null);

    fetch(API)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
        return res.json();
      })
      .then(data => {
        // Sort alphabetically
        const sorted = data.sort((a, b) =>
          a.name.common.localeCompare(b.name.common)
        );
        setCountries(sorted);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchCountries();
  }, []);

  // Filter logic — runs every render, but that's fine for small arrays
  const filtered = countries.filter(c => {
    const matchSearch = c.name.common.toLowerCase().includes(search.toLowerCase());
    const matchRegion = region === "All" || c.region === region;
    return matchSearch && matchRegion;
  });

  return (
    <div style={{ padding: "1.5rem 1rem", maxWidth: 960, margin: "0 auto" }}>

      {/* Header */}
      <div style={{ marginBottom: "1.5rem" }}>
        <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)" }}>
          🌍 Country Explorer
        </h1>
        <p style={{ margin: 0, fontSize: 13, color: "var(--color-text-secondary)" }}>
          Fetches from REST Countries API · search · filter by region
        </p>
      </div>

      {/* Controls — search + filter live here, state is "lifted up" to this component */}
      {!loading && !error && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: "1.5rem" }}>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <SearchBox value={search} onChange={setSearch} />
            {(search || region !== "All") && (
              <button
                onClick={() => { setSearch(""); setRegion("All"); }}
                style={{ fontSize: 12, whiteSpace: "nowrap", color: "var(--color-text-secondary)" }}
              >
                Clear ×
              </button>
            )}
          </div>
          <RegionFilter selected={region} onChange={setRegion} />

          {/* Result count */}
          <p style={{ margin: 0, fontSize: 11, color: "var(--color-text-secondary)" }}>
            Showing {filtered.length} of {countries.length} countries
          </p>
        </div>
      )}

      {/* Conditional rendering — show the right UI for each state */}
      {loading && <LoadingState />}
      {error && <ErrorState message={error} onRetry={fetchCountries} />}
      {!loading && !error && filtered.length === 0 && (
        <EmptyState query={search} region={region} />
      )}
      {!loading && !error && filtered.length > 0 && (
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
          gap: 14,
        }}>
          {filtered.map(c => (
            <CountryCard key={c.name.common} country={c} />
          ))}
        </div>
      )}
    </div>
  );
}