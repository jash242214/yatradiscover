'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

interface ApiStatus {
  status: string;
  service: string;
  version: string;
  environment: string;
}

export default function Home() {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkApi = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await axios.get(`${apiUrl}/health`);
        setApiStatus(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to connect to API');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    checkApi();
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-600 to-purple-600">
      {/* Navigation */}
      <nav className="bg-white bg-opacity-10 backdrop-blur-md text-white p-6">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold">🌍 YatraDiscover AI</h1>
          <div className="space-x-6">
            <a href="#features" className="hover:text-indigo-200">Features</a>
            <a href="#api" className="hover:text-indigo-200">API</a>
            <a href="https://github.com/jash242214/yatradiscover" className="hover:text-indigo-200">GitHub</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 py-20 text-white">
        <div className="text-center space-y-6">
          <h2 className="text-6xl font-bold">AI-Powered Travel Planning</h2>
          <p className="text-2xl opacity-90">
            Personalized recommendations, smart itineraries, and seamless bookings
          </p>
          <div className="pt-8 space-x-4">
            <button className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-bold hover:bg-indigo-50 transition">
              Get Started
            </button>
            <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-bold hover:bg-white hover:bg-opacity-10 transition">
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* API Status */}
      <section id="api" className="bg-white bg-opacity-10 backdrop-blur-md py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h3 className="text-3xl font-bold text-white mb-8">API Status</h3>
          <div className="bg-white rounded-lg p-8 shadow-lg">
            {loading && (
              <div className="text-center py-8">
                <div className="inline-block animate-spin">⏳</div>
                <p className="text-gray-600 mt-4">Connecting to API...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded">
                <p className="font-semibold">❌ {error}</p>
                <p className="text-sm mt-2">Make sure the backend is running at {process.env.NEXT_PUBLIC_API_URL}</p>
              </div>
            )}

            {apiStatus && (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-green-50 rounded border border-green-200">
                  <span className="text-gray-700 font-semibold">Status</span>
                  <span className="text-green-600 font-bold">✅ {apiStatus.status.toUpperCase()}</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-blue-50 rounded border border-blue-200">
                  <span className="text-gray-700 font-semibold">Service</span>
                  <span className="text-blue-600 font-bold">{apiStatus.service}</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-purple-50 rounded border border-purple-200">
                  <span className="text-gray-700 font-semibold">Version</span>
                  <span className="text-purple-600 font-bold">{apiStatus.version}</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-indigo-50 rounded border border-indigo-200">
                  <span className="text-gray-700 font-semibold">Environment</span>
                  <span className="text-indigo-600 font-bold">{apiStatus.environment}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="max-w-6xl mx-auto px-6 py-20">
        <h3 className="text-3xl font-bold text-white text-center mb-12">Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: '🤖',
              title: 'AI Recommendations',
              desc: 'Personalized travel suggestions powered by OpenAI'
            },
            {
              icon: '🗺️',
              title: 'Smart Planning',
              desc: 'Multi-city itineraries with real-time optimization'
            },
            {
              icon: '💳',
              title: 'Easy Bookings',
              desc: 'Integrated hotel, flight, and restaurant reservations'
            },
            {
              icon: '👥',
              title: 'Group Travel',
              desc: 'Collaborate with friends and family in real-time'
            },
            {
              icon: '💰',
              title: 'Budget Planning',
              desc: 'Smart budget allocation and expense tracking'
            },
            {
              icon: '🔒',
              title: 'Secure & Private',
              desc: 'End-to-end encryption for all your travel data'
            },
          ].map((feature, idx) => (
            <div key={idx} className="bg-white bg-opacity-10 backdrop-blur-md rounded-lg p-8 text-white hover:bg-opacity-20 transition">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h4 className="text-xl font-bold mb-2">{feature.title}</h4>
              <p className="opacity-90">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-white bg-opacity-10 backdrop-blur-md py-16 text-center text-white">
        <div className="max-w-4xl mx-auto px-6">
          <h3 className="text-4xl font-bold mb-6">Ready to Plan Your Adventure?</h3>
          <p className="text-xl opacity-90 mb-8">
            Join thousands of travelers discovering amazing destinations with AI
          </p>
          <button className="bg-white text-indigo-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-indigo-50 transition">
            Start Planning Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black bg-opacity-30 text-white py-8 border-t border-white border-opacity-10">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p>&copy; 2026 YatraDiscover AI. All rights reserved.</p>
          <p className="text-sm opacity-75 mt-2">Powered by Next.js, FastAPI, and OpenAI</p>
        </div>
      </footer>
    </main>
  );
}
