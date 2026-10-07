#!/usr/bin/env python3
"""
Generate publication-quality SVG figures for the manuscript:
1. pta_lorentzian_profile.svg - Lorentzian line broadening across galactic radii.
2. core_halo_bifurcation.svg - Pristine quantum dwarf core vs decohered disk core scaling.
"""

import math
import os

DIR = os.path.dirname(os.path.abspath(__file__))

def generate_pta_svg():
    width, height = 700, 450
    margin_left, margin_bottom, margin_top, margin_right = 90, 70, 50, 40
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    f0 = 48.36  # nHz
    freqs = [f0 + df for df in [-1.5, -1.0, -0.6, -0.4, -0.2, -0.1, -0.05, 0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 1.0, 1.5]]
    # Evaluate three representative curves:
    # 1. Nuclear Cluster (broad)
    # 2. Inner Disk (medium)
    # 3. Solar Neighborhood (sharp)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;">']
    svg.append(f'<text x="{width//2}" y="30" font-size="16" font-weight="bold" text-anchor="middle" fill="#111827">Pulsar Timing Power Spectral Density: Quantum Tidal Line Broadening</text>')

    # Axes
    x0, y0 = margin_left, margin_top + plot_h
    x1, y1 = margin_left + plot_w, margin_top
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#374151" stroke-width="2"/>')
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#374151" stroke-width="2"/>')

    # Grid & labels
    svg.append(f'<text x="{margin_left + plot_w//2}" y="{height - 20}" font-size="13" font-weight="600" text-anchor="middle" fill="#374151">Frequency f [nHz] (around f0 = 48.36 nHz)</text>')
    svg.append(f'<text transform="rotate(-90)" x="-{margin_top + plot_h//2}" y="30" font-size="13" font-weight="600" text-anchor="middle" fill="#374151">Power Spectral Density S(f) [arbitrary units]</text>')

    # Plot curves
    def lorentzian(f, f_center, gamma):
        return (gamma / (2 * math.pi)) / ((f - f_center)**2 + (gamma / 2)**2)

    profiles = [
        {"name": "Nuclear Cluster (R = 0.05 kpc, gamma = 0.8 nHz)", "gamma": 0.8, "color": "#dc2626"},
        {"name": "Inner Disk (R = 1.5 kpc, gamma = 0.3 nHz)", "gamma": 0.3, "color": "#2563eb"},
        {"name": "Solar Circle (R = 8.5 kpc, sharp)", "gamma": 0.08, "color": "#16a34a"},
    ]

    f_min, f_max = 46.5, 50.2
    n_pts = 200
    df_step = (f_max - f_min) / n_pts

    for prof in profiles:
        gamma = prof["gamma"]
        pts = []
        for i in range(n_pts + 1):
            f_val = f_min + i * df_step
            val = lorentzian(f_val, f0, gamma)
            # Normalize peak to ~300 px
            norm_val = min(plot_h - 20, val * 220 * gamma)
            px = x0 + (f_val - f_min) / (f_max - f_min) * plot_w
            py = y0 - norm_val
            pts.append(f"{px:.1f},{py:.1f}")
        svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{prof["color"]}" stroke-width="2.5"/>')

    # Legend
    leg_x = margin_left + 30
    leg_y = margin_top + 30
    for i, prof in enumerate(profiles):
        svg.append(f'<line x1="{leg_x}" y1="{leg_y + i*22}" x2="{leg_x + 25}" y2="{leg_y + i*22}" stroke="{prof["color"]}" stroke-width="3"/>')
        svg.append(f'<text x="{leg_x + 35}" y="{leg_y + i*22 + 4}" font-size="12" fill="#1f2937">{prof["name"]}</text>')

    svg.append('</svg>')
    out_path = os.path.join(DIR, "pta_lorentzian_profile.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_pta_svg()
