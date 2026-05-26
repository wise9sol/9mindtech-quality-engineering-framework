"use client";

import Image from "next/image";
import { useState } from "react";

interface BrandLogoProps {
  height: number;
  className?: string;
  priority?: boolean;
}

export default function BrandLogo({ height, className = "", priority = false }: BrandLogoProps) {
  const [imgError, setImgError] = useState(false);

  if (imgError) {
    return (
      <span
        className={`font-bold tracking-tight ${className}`}
        style={{ fontSize: Math.max(11, height * 0.38), lineHeight: 1 }}
      >
        <span style={{ color: "#6366f1" }}>QualiOps</span>{" "}
        <span style={{ color: "#a855f7" }}>AI</span>
      </span>
    );
  }

  return (
    <Image
      src="/logo.png"
      alt="QualiOps AI by 9MindTech"
      width={400}
      height={120}
      priority={priority}
      onError={() => setImgError(true)}
      style={{ height: `${height}px`, width: "auto" }}
      className={className}
    />
  );
}