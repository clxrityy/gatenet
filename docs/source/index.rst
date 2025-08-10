.. raw:: html

   <section class="hero" style="margin-top: 3.5rem;">
     <div class="hero-content">
       <h1>Gatenet</h1>
       <p>Async-first Python networking toolkit: sockets, HTTP, diagnostics, discovery, mesh networking, and hardware microservices.<br>
       <b>Now with LoRa, ESP, Wi-Fi, GPS, SDR, and extensible protocol support.</b></p>
       <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 1.5rem; gap: 0.5rem;">
         <a href="https://github.com/clxrityy/gatenet" target="_blank" style="display: inline-flex; align-items: center; gap: 0.5em; background: #f5f5f5; color: #24292f; border: 1px solid #d1d5da; border-radius: 5px; padding: 0.4em 1em; font-size: 1em; font-family: 'Fira Mono', 'Menlo', 'Consolas', monospace; text-decoration: none; box-shadow: none; transition: background 0.2s;">
           <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 0.5em;"><path d="M12 2C6.48 2 2 6.58 2 12.26c0 4.49 2.87 8.3 6.84 9.64.5.09.68-.22.68-.48 0-.24-.01-.87-.01-1.7-2.78.62-3.37-1.36-3.37-1.36-.45-1.18-1.1-1.5-1.1-1.5-.9-.63.07-.62.07-.62 1 .07 1.53 1.05 1.53 1.05.89 1.56 2.34 1.11 2.91.85.09-.66.35-1.11.63-1.37-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.7 0 0 .84-.28 2.75 1.05A9.38 9.38 0 0 1 12 6.8c.85.004 1.7.12 2.5.34 1.9-1.33 2.74-1.05 2.74-1.05.55 1.4.2 2.44.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9 0 1.37-.01 2.47-.01 2.8 0 .26.18.57.69.48A10.01 10.01 0 0 0 22 12.26C22 6.58 17.52 2 12 2Z" fill="#24292f"/></svg>
           GitHub
         </a>
         <pre class="hero-install-block" style="margin: 0.5em 0 0 0; background: #222b36; color: #fff; border-radius: 6px; padding: 0.5em 1em; font-size: 1.05em; font-family: 'Fira Mono', 'Menlo', 'Consolas', monospace; box-shadow: 0 2px 8px 0 rgba(30,40,60,0.07); border: 1px solid #232946;">pip install gatenet</pre>
       </div>
       <div class="hero-details" style="margin-top: 1.5em; margin-bottom: 1.5em; background: linear-gradient(135deg, rgba(240,240,245,0.08) 0%, rgba(200,200,220,0.04) 100%); border-radius: 8px; padding: 1em 1.5em; box-shadow: 0 2px 8px 0 rgba(30,40,60,0.05); font-size: 0.85em; color: inherit; max-width: 700px;">
        <ul style="margin: 0; padding: 0; text-align: left;">
          <li><b>Modular architecture:</b> TCP/UDP/HTTP clients & servers, diagnostics, service discovery, mesh networking, dashboard, and utilities.</li>
          <li><b>Extensible design:</b> Strategy & chain-of-responsibility patterns, abstract base classes, and fluent APIs for easy customization.</li>
          <li><b>Diagnostics suite:</b> Ping, traceroute, bandwidth, geo IP, DNS, port scanning, and more.</li>
          <li><b>Service discovery:</b> SSH, HTTP, FTP, SMTP, mDNS, Bluetooth, UPNP, and custom detectors.</li>
          <li><b>Mesh networking:</b> Modular mesh with LoRa, ESP, Wi-Fi, GPS, SDR, encrypted messaging, topology mapping, and log syncing.</li>
          <li><b>Live dashboard:</b> FastAPI-powered web dashboard for diagnostics and real-time output.</li>
          <li><b>Async-first & testable:</b> Modern async/await support, robust test coverage, and easy integration.</li>
          <li><b>Hardware integration:</b> LoRa, ESP, Wi-Fi, GPS, SDR, and extensible protocol support.</li>
        </ul>
      </div>
     </div>
     <div>
       <img src="_static/coverage.svg" alt="Coverage Badge" class="hero-coverage-badge" />
     </div>
     <div class="hero-animation">
       <!-- Animated Satellite SVG -->
       <div class="satellite-orbit">
         <svg class="satellite-svg" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 6.827 6.827">
           <g>
             <path class="fil0" style="fill:#01579b" transform="rotate(45 -2.537 6.318) scale(1.06075)" d="M0 0h.64v.107H0z"/>
             <path class="fil0" style="fill:#01579b" transform="rotate(45 -1.78 4.49) scale(1.06075)" d="M0 0h.64v.107H0z"/>
             <path class="fil1" style="fill:#0277bd" transform="rotate(45 -2.265 6.888) scale(1.0848 .93548)" d="M0 0h2.302v.89H0z"/>
             <path class="fil2" style="fill:#eee" d="m4.208 3.618.295.294v.002l-.295.294v.001h-.002l-.294-.295h-.001l.001-.002.294-.294.001-.001h.001zm.292.295-.293-.292-.292.292.292.292.293-.292z"/>
             <path class="fil2" style="fill:#eee" d="m4.794 4.207-.292-.292-.293.292.293.293.292-.293zm-.291-.295.294.294.001.001-.001.001-.294.295H4.5l-.295-.295v-.002l.295-.294v-.001l.002.001z"/>
             <path class="fil2" style="fill:#eee" d="m4.797 4.206.294.295h.001v.002l-.295.294-.001.001-.001-.001-.294-.294-.001-.001V4.5l.295-.295h.002zm.291.296-.292-.293-.292.293.292.292.292-.292z"/>
             <path class="fil2" style="fill:#eee" d="m5.382 4.796-.292-.292-.292.292.292.292.292-.292zm-.29-.295.294.294v.002l-.295.294v.001h-.002l-.294-.295-.001-.001v-.001L5.09 4.5 5.09 4.5h.001z"/>
             <path class="fil2" style="fill:#eee" d="m5.386 4.795.294.294.001.001-.001.001-.294.295h-.002l-.295-.295v-.002l.295-.294v-.001h.002zm.29.295-.291-.292-.293.292.293.292.292-.292z"/>
             <path class="fil2" style="fill:#eee" d="m5.971 5.385-.292-.293-.292.293.292.292.292-.292zm-.291-.296.294.295h.001v.002l-.295.294-.001.001-.001-.001-.294-.294-.002-.001.002-.001.294-.295h.002zM3.62 4.207l.293.293.292-.293-.292-.292-.292.292zm.292.296-.294-.295h-.001v-.002l.295-.294.001-.001.001.001.294.294.001.001v.001l-.295.295h-.002z"/>
             <path class="fil2" style="fill:#eee" d="m4.206 4.797-.294-.294-.001-.001.001-.001.294-.295h.002l.295.295v.002l-.295.294v.001l-.002-.001zm-.29-.295.291.292.293-.292-.293-.293-.292.293z"/>
             <path class="fil2" style="fill:#eee" d="m4.21 4.796.292.292.292-.292-.292-.292-.292.292zm.29.295-.294-.294v-.002l.295-.294V4.5h.002l.294.295.001.001-.001.001-.294.294-.001.001H4.5z"/>
             <path class="fil2" style="fill:#eee" d="M4.795 5.386 4.5 5.09H4.5v-.002l.295-.294.001-.001h.001l.294.295.001.001v.001l-.295.295h-.002zm-.291-.296.292.292.292-.292-.292-.292-.292.292z"/>
             <path class="fil2" style="fill:#eee" d="m4.798 5.385.292.292.292-.292-.292-.293-.292.293zm.291.295-.294-.294-.001-.001v-.001l.295-.295h.002l.295.295v.002l-.295.294v.001l-.002-.001z"/>
             <path class="fil2" style="fill:#eee" d="m5.384 5.974-.295-.294v-.002l.295-.294v-.002l.002.002.294.294h.001l-.001.002-.294.294-.001.001h-.001zm-.292-.295.293.292.292-.292-.292-.292-.293.292z"/>
             <path class="fil1" style="fill:#0277bd" transform="rotate(45 -.31 2.167) scale(1.0848 .93548)" d="M0 0h2.302v.89H0z"/>
             <path class="fil2" style="fill:#eee" d="m1.443.852.294.295h.001v.002l-.295.294-.001.001-.001-.001-.294-.294-.001-.001v-.001l.295-.295h.002zm.291.296L1.442.855l-.292.293.292.292.292-.292z"/>
             <path class="fil2" style="fill:#eee" d="m2.028 1.442-.292-.292-.292.292.292.292.292-.292zm-.29-.295.294.294v.002l-.295.294v.001h-.002l-.294-.295-.001-.001V1.44l.295-.294.001-.001h.001z"/>
             <path class="fil2" style="fill:#eee" d="m2.032 1.44.294.295v.002l-.294.295h-.003l-.294-.295v-.002l.294-.294.002-.001zm.29.296-.291-.292-.293.292.293.292.292-.292z"/>
             <path class="fil2" style="fill:#eee" d="m2.617 2.03-.292-.292-.292.293.292.292.292-.292zm-.291-.295.294.294.001.002-.295.295h-.002l-.295-.294v-.003l.295-.294h.002z"/>
             <path class="fil2" style="fill:#eee" d="m2.62 2.03.294.294h.002l-.002.002-.294.294v.001h-.002l-.294-.295-.001-.001v-.001l.295-.295h.002zm.291.295-.292-.292-.292.292.292.292.292-.292z"/>
             <path class="fil2" style="fill:#eee" d="m3.206 2.62-.293-.293-.292.292.292.292.293-.292zm-.292-.296.295.294v.002l-.295.294v.002l-.002-.002-.294-.294h-.001l.001-.002.294-.294.001-.001h.001zM.855 1.442l.293.292.292-.292-.292-.292-.293.292zm.292.295-.295-.294v-.002l.295-.294v-.001h.002l.294.295h.001l-.001.002-.294.294-.001.001h-.001z"/>
             <path class="fil2" style="fill:#eee" d="m1.44 2.032-.293-.295h-.001v-.002l.295-.294V1.44h.002l.294.295.001.001v.001l-.295.295h-.002zm-.29-.296.292.292.292-.292-.292-.292-.292.292z"/>
             <path class="fil2" style="fill:#eee" d="m1.444 2.03.292.293.292-.292-.292-.293-.292.293zm.291.296-.294-.294-.001-.001v-.002l.295-.294h.002l.295.294v.002l-.295.295h-.002z"/>
             <path class="fil2" style="fill:#eee" d="m2.03 2.62-.295-.294v-.002l.294-.295h.002l.295.295v.002l-.294.294-.001.001h-.002zm-.292-.295.293.292.292-.292-.292-.292-.293.292z"/>
             <path class="fil2" style="fill:#eee" d="m2.033 2.62.292.291.292-.292-.292-.292-.292.292zm.29.294L2.03 2.62v-.002l.295-.294v-.001h.002l.294.295.001.001v.001l-.295.294-.001.002-.001-.002z"/>
             <path class="fil2" style="fill:#eee" d="m2.618 3.209-.294-.295h-.001v-.002l.295-.294.001-.001.001.001.294.294.002.001-.002.001-.294.295h-.002zm-.291-.296.292.293.292-.293-.292-.292-.292.292z"/>
             <path class="fil3" style="fill:#616161" d="m3.768 2.459.6.6c.055.055.065.135.022.178L2.983 4.643c-.043.043-.123.034-.178-.021l-.6-.6c-.055-.056-.065-.136-.022-.179L3.59 2.437c.043-.043.123-.033.178.022z"/>
             <path class="fil3" style="fill:#616161" d="m4.068 2.759.003.002.297.298c.055.055.065.135.022.178L2.983 4.643c-.043.043-.123.034-.178-.021l-.3-.3 1.563-1.563z"/>
             <path style="fill:#757575" d="m3.768 2.459.3.3-1.563 1.563-.3-.3c-.055-.056-.065-.136-.022-.179L3.59 2.437c.043-.043.123-.033.178.022z"/>
             <g>
               <path style="fill:#283593;fill-rule:nonzero" d="m2.032 4.86-.388.387-.065-.065.388-.387z"/>
               <path style="fill:#283593;fill-rule:nonzero" d="M1.678 4.366v.857h-.092v-.857z"/>
               <path style="fill:#283593;fill-rule:nonzero" d="M2.478 5.166v.092H1.62v-.092z"/>
               <path style="fill:#424242" d="M1.3 4.22a.937.937 0 0 1 1.306 1.307L1.3 4.22z"/>
               <path style="fill:#3b3b3b" d="M2.505 4.321l.002.003c.327.328.36.838.1 1.203l-.653-.652-.001-.001.552-.553z"/>
               <path style="fill:#424242" d="M1.3 4.22a.937.937 0 0 1 1.205.101l-.552.553L1.3 4.22z"/>
               <circle transform="rotate(45 -5.455 4.567) scale(2.12135)" r=".053" style="fill:#bf360c"/>
             </g>
           </g>
           <path style="fill:none" d="M0 0h6.827v6.827H0z"/>
         </svg>
       </div>
     </div>
   </section>

.. toctree::
   :maxdepth: 4
   :caption: API Reference

   modules

.. toctree::
   :maxdepth: 1
   :caption: Project Overview

   examples
   sandbox
   coverage_summary
   changelog
   security

.. toctree::
   :maxdepth: 1
   :caption: Resources

   cli
   hardware_setup
   cli_integration_examples
   advanced_radio_usage
   hotspot_usage