"use client";

import { useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Sidebar from "@/components/layout/Sidebar";
import MobileNav from "@/components/layout/MobileNav";
import PageContainer from "@/components/layout/PageContainer";
import TripInput from "@/components/planner/TripInput";
import AgentProgress from "@/components/planner/AgentProgress";
import PlanningProcess from "@/components/planner/PlanningProcess";
import ItineraryView from "@/components/itinerary/ItineraryView";
import ChatContainer from "@/components/chat/ChatContainer";
import ChatInput from "@/components/chat/ChatInput";
import QuickActions from "@/components/chat/QuickActions";
import EmptyState from "@/components/common/EmptyState";
import ErrorState from "@/components/common/ErrorState";
import Loading from "@/components/common/Loading";
import { useHistory } from "@/hooks/useHistory";
import { useTrip } from "@/hooks/useTrip";
import { useChat } from "@/hooks/useChat";

export default function HomePage() {
  const { history, saveTrip, removeTrip } = useHistory();
  const { trip, loading, error, generate, setTrip } = useTrip();
  const { messages, loading: chatLoading, sendMessage, resetMessages } = useChat();
  const [currentTripQuestion, setCurrentTripQuestion] = useState("");

  async function handleGenerate(question: string) {
    resetMessages();
    setCurrentTripQuestion("");
    setTrip(null);
    const createdTrip = await generate(question, saveTrip);
    if (createdTrip) {
      setCurrentTripQuestion(createdTrip.question);
    }
  }

  async function handleChat(message: string) {
    if (!currentTripQuestion || !trip) {
      await handleGenerate(message);
      return;
    }

    const result = await sendMessage(message, currentTripQuestion, trip.answer);

    if (result?.answer && trip) {
      const updatedTrip = { ...trip, answer: result.answer };
      setTrip(updatedTrip);
      saveTrip(updatedTrip);
    }
  }

  function handleNewTrip() {
    resetMessages();
    setCurrentTripQuestion("");
    window.location.href = "/";
  }

  async function handleAction(action: string) {
    await handleChat(action);
  }

  return (
    <div className="app-shell">
      <Sidebar history={history} onNewTrip={handleNewTrip} onDeleteTrip={removeTrip} />

      <div className="app-main">
        <Navbar />

        <PageContainer>
          <section className="hero">
            <div className="hero-glow hero-glow-one" />
            <div className="hero-glow hero-glow-two" />

            <div className="hero-content">
              <div className="hero-badge">Intelligent travel planning</div>

              <h1>
                Plan smarter.
                <br />
                Travel better.
              </h1>

              <p>
                Generate, evaluate, and refine travel itineraries using an
                agentic AI workflow.
              </p>
            </div>

          </section>

          <TripInput onSubmit={handleGenerate} loading={loading} />

          <PlanningProcess />

          <AgentProgress active={loading} />

          {loading && <Loading label="Your travel agent is working..." />}

          {error && <ErrorState message={error} />}

          {trip && (
            <>
              <ItineraryView answer={trip.answer} />

              <section className="chat-section">
                <div className="section-title">
                  <span>Continue the conversation</span>
                </div>

                <ChatContainer messages={messages} />

                <QuickActions onSelect={handleAction} />

                <ChatInput
                  onSend={handleChat}
                  disabled={chatLoading}
                />
              </section>
            </>
          )}

          {!trip && !loading && !error && <EmptyState />}
        </PageContainer>

        <MobileNav onNewTrip={handleNewTrip} />
      </div>
    </div>
  );
}