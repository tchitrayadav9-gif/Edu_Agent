"""
Test suite for Short-Term & Long-Term Memory Systems.
Proves that information from a previous interaction is permanently remembered
and correctly retrieved during a later interaction.
"""

import pytest
from backend.app.memory.short_term_memory import short_term_memory
from backend.app.memory.long_term_memory import long_term_memory
from backend.app.memory.memory_manager import memory_manager
from backend.app.memory.memory_retriever import memory_retriever


@pytest.fixture(autouse=True)
def clean_memory():
    long_term_memory.clear_user_memories("test_student_101")


def test_short_term_memory_buffer():
    conv_id = "test_conv_abc"
    short_term_memory.clear(conv_id)
    short_term_memory.add_turn(conv_id, "user", "My goal is AI Engineer")
    short_term_memory.add_turn(conv_id, "assistant", "Noted!")
    
    turns = short_term_memory.get_recent_turns(conv_id)
    assert len(turns) == 2
    assert turns[0]["role"] == "user"
    assert "AI Engineer" in turns[0]["content"]


def test_auto_fact_extraction_and_persistence():
    user_id = "test_student_101"
    user_text = "My name is Chitra. I want to become an AI Engineer. I know Python but I am weak in Machine Learning."
    
    facts = memory_manager.extract_facts_from_text(user_text, user_id)
    assert len(facts) >= 3
    
    types = [f["memory_type"] for f in facts]
    assert "career_goal" in types
    assert "skill" in types
    assert "weakness" in types


def test_cross_session_memory_retrieval():
    """
    CRITICAL TEST:
    Interaction 1: User declares career goal and weakness.
    Interaction 2: Later, user asks 'What should I learn next?'
    Verify that memory retrieval returns the target career goal and weak skills.
    """
    user_id = "test_student_101"
    conv_1 = "session_turn_01"
    conv_2 = "session_turn_02"

    # Turn 1: Save facts
    memory_manager.process_turn(
        user_id=user_id,
        conversation_id=conv_1,
        user_message="I want to become an AI Engineer. I am weak in Statistics.",
        agent_response="Great, I have noted your career goal as AI Engineer and Statistics as a weak area."
    )

    # Verify long term storage
    all_memories = long_term_memory.get_all_memories(user_id)
    assert len(all_memories) >= 2

    # Turn 2: Later query
    query_2 = "What should I learn next?"
    retrieved = memory_retriever.retrieve_relevant_memories(user_id, query_2, top_k=3)
    
    assert len(retrieved) > 0
    retrieved_content = " ".join([m["content"] for m in retrieved])
    assert "AI Engineer" in retrieved_content or "Statistics" in retrieved_content


def test_memory_update_conflict_resolution():
    user_id = "test_student_101"
    
    # Store initial goal
    long_term_memory.save_memory(user_id, "career_goal", "Target Career Goal is Data Scientist.")
    
    # Update to new goal
    long_term_memory.save_memory(user_id, "career_goal", "Target Career Goal is AI Engineer.")
    
    career_memories = long_term_memory.get_memories_by_type(user_id, "career_goal")
    assert len(career_memories) == 1
    assert "AI Engineer" in career_memories[0]["content"]
