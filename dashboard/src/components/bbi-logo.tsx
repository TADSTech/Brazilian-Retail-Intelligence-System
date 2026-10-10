interface BbiLogoProps {
  className?: string;
}

// BrazilBI mark: cobalt tile, ascending bars (retail growth),
// amber dot (Brazil star / peak data point). Decorative — pair with text.
export function BbiLogo({ className = 'size-8' }: BbiLogoProps) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden focusable="false">
      <defs>
        <linearGradient id="bbi-tile" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#3C8CF0" />
          <stop offset="1" stopColor="#0053B4" />
        </linearGradient>
      </defs>
      <rect width="32" height="32" rx="7.5" fill="url(#bbi-tile)" />
      <g fill="#FFFFFF">
        <rect x="6" y="16.5" width="4.5" height="7" rx="2.25" />
        <rect x="12.5" y="12" width="4.5" height="11.5" rx="2.25" />
        <rect x="19" y="7" width="4.5" height="16.5" rx="2.25" />
      </g>
      <circle cx="26.4" cy="8.8" r="2.3" fill="#FACC15" />
    </svg>
  );
}
