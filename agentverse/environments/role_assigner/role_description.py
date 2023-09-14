from __future__ import annotations

from typing import TYPE_CHECKING, List

from . import role_assigner_registry
from .base import BaseRoleAssigner

if TYPE_CHECKING:
    from agentverse.message import RoleAssignerMessage
    from agentverse.agents import CriticAgent, RoleAssignerAgent


@role_assigner_registry.register("role_description")
class DescriptionAssigner(BaseRoleAssigner):
    """
    Generates descriptions for each agent.
    """

    cnt_agents: int = 0

    def step(
        self,
        role_assigner: RoleAssignerAgent,
        group_members: List[CriticAgent],
        advice: str = "No advice yet.",
        task_description: str = "",
        *args,
        **kwargs,
    ) -> List[CriticAgent]:
        assert task_description != ""
        assert self.cnt_agents > 0

        roles = role_assigner.step(advice, task_description, self.cnt_agents)
        if len(roles.content) < len(group_members):
            raise ValueError(
                f"Number of roles ({len(roles.content)}) and number of group members ({len(group_members)}) do not match."
            )
        for role, member in zip(roles.content[: len(group_members)], group_members):
            description = role.strip().strip(".")
            member.role_description = description
            member.name = description

        return group_members

    def reset(self):
        pass
