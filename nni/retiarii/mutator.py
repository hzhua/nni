from typing import (Any, Iterable, List, Optional)

from .graph import Model


__all__ = ['Sampler', 'Mutator']


Choice = Any


class Sampler:
    """
    Handles `Mutator.choice()` calls.
    """
    def choice(self, candidates: List[Choice], mutator: 'Mutator', model: Model, index: int) -> Choice:
        raise NotImplementedError()

    def mutation_start(self, mutator: 'Mutator', model: Model) -> None:
        pass

    def mutation_end(self, mutator: 'Mutator', model: Model) -> None:
        pass


class Mutator:
    """
    Mutates graphs in model to generate new model.
    `Mutator` class will be used in two places:
      1. Inherit `Mutator` to implement graph mutation logic.
      2. Use `Mutator` subclass to implement NAS strategy.
    In scenario 1, the subclass should implement `Mutator.mutate()` interface with `Mutator.choice()`.
    In scenario 2, strategy should use constructor or `Mutator.bind_sampler()` to initialize subclass,
    and then use `Mutator.apply()` to mutate model.
    For certain mutator subclasses, strategy or sampler can use `Mutator.dry_run()` to predict choice candidates.
    # Method names are open for discussion.
    """
    def __init__(self, sampler: Optional[Sampler] = None):
        self.sampler: Optional[Sampler] = sampler
        self._cur_model: Optional[Model] = None
        self._cur_choice_idx: Optional[int] = None

    def bind_sampler(self, sampler: Sampler) -> 'Mutator':
        """
        Set the sampler which will handle `Mutator.choice` calls.
        """
        self.sampler = sampler
        return self

    def apply(self, model: Model) -> Model:
        """
        Apply this mutator on a model.
        Returns mutated model.
        The model will be copied before mutation and the original model will not be modified.
        """
        assert self.sampler is not None
        copy = model.fork()
        self._cur_model = copy
        self._cur_choice_idx = 0
        self.sampler.mutation_start(self, copy)
        self.mutate(copy)
        self.sampler.mutation_end(self, copy)
        self._cur_model = None
        self._cur_choice_idx = None
        return copy

    def dry_run(self, model: Model) -> List[List[Choice]]:
        """
        Dry run mutator on a model to collect choice candidates.
        If you invoke this method multiple times on same or different models,
        it may or may not return identical results, depending on how the subclass implements `Mutator.mutate()`.
        """
        sampler_backup = self.sampler
        recorder = _RecorderSampler()
        self.sampler = recorder
        self.apply(model)
        self.sampler = sampler_backup
        return recorder.recorded_candidates


    def mutate(self, model: Model) -> None:
        """
        Abstract method to be implemented by subclass.
        Mutate a model in place.
        """
        raise NotImplementedError()

    def choice(self, candidates: Iterable[Choice]) -> Choice:
        """
        Ask sampler to make a choice.
        """
        assert self.sampler is not None and self._cur_model is not None and self._cur_choice_idx is not None
        ret = self.sampler.choice(list(candidates), self, self._cur_model, self._cur_choice_idx)
        self._cur_choice_idx += 1
        return ret


class _RecorderSampler(Sampler):
    def __init__(self):
        self.recorded_candidates: List[List[Choice]] = []

    def choice(self, candidates: List[Choice], *args) -> Choice:
        self.recorded_candidates.append(candidates)
        return candidates[0]