// ProfileCardGallery.jsx
// Built while learning React – Session 4:30–6:00
// Topics: components, props, array.map(), responsive layout

import { useState } from "react";

// --- DATA ---
// I learned that keeping data separate from UI is good practice!
const profiles = [
  {
    id: 1,
    name: "Aisha Patel",
    role: "Frontend Developer",
    location: "Mumbai, India",
    bio: "I love making things look good on screens. Currently learning React and CSS grid.",
    skills: ["HTML", "CSS", "React"],
    avatar: "AP",
    color: "#6C63FF",
  },
  {
    id: 2,
    name: "Carlos Rivera",
    role: "UI/UX Designer",
    location: "Mexico City",
    bio: "Designer who codes a little. Figma is my best friend. Working on my portfolio.",
    skills: ["Figma", "Tailwind", "Prototyping"],
    avatar: "CR",
    color: "#E8645A",
  },
  {
    id: 3,
    name: "Priya Sharma",
    role: "CS Student",
    location: "Jaipur, India",
    bio: "2nd year student building projects to learn. This card gallery is one of them!",
    skills: ["Python", "JavaScript", "Git"],
    avatar: "PS",
    color: "#0EA5A0",
  },
  {
    id: 4,
    name: "Luca Bianchi",
    role: "Backend Dev",
    location: "Rome, Italy",
    bio: "I make APIs. Finally trying to understand why CSS is the way it is.",
    skills: ["Node.js", "PostgreSQL", "REST"],
    avatar: "LB",
    color: "#F59E0B",
  },
  {
    id: 5,
    name: "Sara Kim",
    role: "Junior Developer",
    location: "Seoul, South Korea",
    bio: "Bootcamp grad. Building one small project every week to keep improving.",
    skills: ["React", "Express", "MongoDB"],
    avatar: "SK",
    color: "#10B981",
  },
  {
    id: 6,
    name: "Omar Hassan",
    role: "Freelance Dev",
    location: "Cairo, Egypt",
    bio: "Self-taught. Love open source. Always happy to help beginners.",
    skills: ["Vue.js", "Django", "Linux"],
    avatar: "OH",
    color: "#8B5CF6",
  },
];

// --- SMALL COMPONENTS ---
// I learned: break UI into small pieces, each does one job

// Avatar circle with initials
function Avatar({ initials, color }) {
  return (
    <div
      style={{
        width: 56,
        height: 56,
        borderRadius: "50%",
        backgroundColor: color + "22", // light tint
        border: `2px solid ${color}`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontWeight: 600,
        fontSize: 16,
        color: color,
        flexShrink: 0,
        letterSpacing: 1,
      }}
    >
      {initials}
    </div>
  );
}

// A single skill badge
function SkillBadge({ skill, color }) {
  return (
    <span
      style={{
        padding: "3px 10px",
        borderRadius: 20,
        fontSize: 11,
        fontWeight: 500,
        backgroundColor: color + "18",
        color: color,
        border: `1px solid ${color}40`,
        whiteSpace: "nowrap",
      }}
    >
      {skill}
    </span>
  );
}

// The full card for one person
function ProfileCard({ profile }) {
  const [liked, setLiked] = useState(false);

  return (
    <div
      style={{
        background: "var(--color-background-primary)",
        border: "1px solid var(--color-border-tertiary)",
        borderRadius: 14,
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: 14,
        transition: "transform 0.15s ease, box-shadow 0.15s ease",
        cursor: "default",
        position: "relative",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-3px)";
        e.currentTarget.style.borderColor = profile.color + "80";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.borderColor = "var(--color-border-tertiary)";
      }}
    >
      {/* Top row: avatar + name */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <Avatar initials={profile.avatar} color={profile.color} />
        <div>
          <p style={{ margin: 0, fontWeight: 600, fontSize: 15, color: "var(--color-text-primary)" }}>
            {profile.name}
          </p>
          <p style={{ margin: 0, fontSize: 12, color: profile.color, fontWeight: 500 }}>
            {profile.role}
          </p>
          <p style={{ margin: "2px 0 0", fontSize: 11, color: "var(--color-text-secondary)" }}>
            📍 {profile.location}
          </p>
        </div>

        {/* Like button — top right */}
        <button
          onClick={() => setLiked(!liked)}
          style={{
            marginLeft: "auto",
            background: "none",
            border: "none",
            cursor: "pointer",
            fontSize: 18,
            padding: 4,
            borderRadius: 6,
            lineHeight: 1,
            opacity: liked ? 1 : 0.35,
            transition: "opacity 0.15s, transform 0.1s",
            transform: liked ? "scale(1.2)" : "scale(1)",
          }}
          title={liked ? "Unlike" : "Like this profile"}
        >
          ❤️
        </button>
      </div>

      {/* Divider */}
      <hr style={{ border: "none", borderTop: "1px solid var(--color-border-tertiary)", margin: 0 }} />

      {/* Bio */}
      <p style={{ margin: 0, fontSize: 13, color: "var(--color-text-secondary)", lineHeight: 1.6 }}>
        {profile.bio}
      </p>

      {/* Skills */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
        {profile.skills.map((skill) => (
          <SkillBadge key={skill} skill={skill} color={profile.color} />
        ))}
      </div>
    </div>
  );
}

// --- MAIN COMPONENT ---
// This is what gets rendered on the page
export default function ProfileCardGallery() {
  return (
    <div style={{ padding: "2rem 1rem", maxWidth: 900, margin: "0 auto" }}>

      {/* Page header */}
      <div style={{ marginBottom: "2rem" }}>
        <h1 style={{ margin: "0 0 6px", fontSize: 24, fontWeight: 700, color: "var(--color-text-primary)" }}>
          👥 Profile Card Gallery
        </h1>
        <p style={{ margin: 0, fontSize: 14, color: "var(--color-text-secondary)" }}>
          Practice project — reusable Card component with responsive grid layout
        </p>
        <div
          style={{
            marginTop: 10,
            display: "inline-block",
            padding: "4px 10px",
            borderRadius: 6,
            fontSize: 11,
            background: "var(--color-background-secondary)",
            color: "var(--color-text-secondary)",
            border: "1px solid var(--color-border-tertiary)",
          }}
        >
          {profiles.length} cards rendered from data array using <code>.map()</code>
        </div>
      </div>

      {/* The responsive grid — this was the tricky part! */}
      {/* auto-fill means it adds columns as space allows */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
          gap: "16px",
        }}
      >
        {profiles.map((profile) => (
          <ProfileCard key={profile.id} profile={profile} />
        ))}
      </div>

      {/* Footer note */}
      <p
        style={{
          marginTop: "2rem",
          textAlign: "center",
          fontSize: 12,
          color: "var(--color-text-secondary)",
          opacity: 0.6,
        }}
      >
        Built while learning React — session 4:30–6:00 ✨
      </p>
    </div>
  );
}