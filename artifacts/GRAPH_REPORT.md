# Graph Report - data/graphify  (2026-06-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 500 nodes · 1071 edges · 28 communities (25 shown, 3 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 258 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8ae2862b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]

## God Nodes (most connected - your core abstractions)
1. `tqdm` - 106 edges
2. `closing()` - 74 edges
3. `TMonitor` - 21 edges
4. `trange()` - 19 edges
5. `Comparable` - 19 edges
6. `TqdmDeprecationWarning` - 18 edges
7. `DiscreteTimer` - 18 edges
8. `TqdmDefaultWriteLock` - 16 edges
9. `Bar` - 16 edges
10. `_OrderedDict` - 16 edges

## Surprising Connections (you probably didn't know these)
- `test_manpath()` --calls--> `main()`  [INFERRED]
  tests/tests_main.py → cli.py
- `test_monitor_thread()` --calls--> `TMonitor`  [INFERRED]
  tests/tests_synchronisation.py → _monitor.py
- `tqdm` --uses--> `TMonitor`  [INFERRED]
  std.py → _monitor.py
- `TqdmDefaultWriteLock` --uses--> `TMonitor`  [INFERRED]
  std.py → _monitor.py
- `test_pandas_apply_args_deprecation()` --calls--> `tqdm_pandas()`  [INFERRED]
  tests/tests_pandas.py → _tqdm_pandas.py

## Import Cycles
- None detected.

## Communities (28 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (50): DeprecationWarning, FutureWarning, RuntimeWarning, test_exceptions(), Test Bar.__format__ spec, test_bar_formatspec(), Thread, cast() (+42 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (32): object, FakeSleep, FakeTqdm, incr(), incr_bar(), make_create_fake_sleep_event(), Test on multiple bars, one not needing miniters adjustment, Wait until the discrete timer reached the required time (+24 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (36): StringIO, Test contrib.tenumerate, test_enumerate(), test_map(), test_zip(), Test pandas.DataFrame.groupby(...).progress_apply, Test pandas with `leave=True`, Test warning info in     `pandas.Dataframe(Series).progress_apply(func, *args)` (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (24): Test time interval format, Test statistics and progress bar formatting, Test SI unit prefixes, test_format_interval(), test_format_meter(), test_si_format(), Formats a number (greater than unity) with SI Order of Magnitude         prefixe, Formats a number of seconds as a clock time, [H:]MM:SS          Parameters (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (26): assert_performance(), checkCpuTime(), cpu_sleep(), MockIO, raises if time_left > thresh * time_right, Test overhead of iteration based tqdm, Test overhead of manual tqdm, Test overhead of nonblocking threads (+18 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (19): BytesIO, IOBase, Null, Test command line pipes, _sh(), test_main(), test_manpath(), Unicode version of StringIO (+11 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (11): KeyError, Test tqdm.keras.TqdmCallback, test_keras(), `keras` callback for epoch and batch progress, Parameters         ----------         epochs  : int, optional         data_size, TqdmCallback, ObjectWrapper, Actual `self.getattr` rather than self._wrapped.getattr (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (11): std_tqdm, Experimental GUI version of tqdm!, A shortcut for `tqdm.gui.tqdm(xrange(*args), **kwargs)`.     On Python3+, `range, tgrange(), tqdm_gui, Resets to 0 iterations for repeated use.          Consider combining with `leave, A shortcut for `tqdm.notebook.tqdm(xrange(*args), **kwargs)`.     On Python3+, `, Experimental IPython/Jupyter Notebook widget using tqdm! (+3 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (18): backendCheck(), # TODO: test degradation on windows without colorama?, Test advance len (numpy array shape), Test redirection of output, Test multiprocess/thread-realted features, # TODO: test interleaved output #445, Test tqdm-like module fallback, Test stripping of ANSI escape codes (+10 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (19): Test adding additional derived format arguments, Test resetting a bar for re-use, Test autodisable will disable on non-TTY, Test numeric `unit_scale`, Test unknown total length, Test manual creation and updates, Test manual creation and closure and n_instances, test_autodisable_disable() (+11 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (6): Restart tqdm timer from last print time., Public API for read-only member access., stream  : file-like object.         method  : str, "read" or "write". The result, Decorate an iterable object, returning an iterator which acts exactly     like t, Registers the given `tqdm` class with             pandas.core.             ( fra, tqdm

### Community 11 - "Community 11"
Cohesion: 0.13
Nodes (12): DummyTqdmFile, Thin wrappers around common functions.  Subpackages contain potentially unstable, Dummy file-like that will write to tqdm, Equivalent of `numpy.ndenumerate` or builtin `enumerate`.      Parameters     --, Equivalent of builtin `zip`.      Parameters     ----------     tqdm_class  : [d, Equivalent of builtin `map`.      Parameters     ----------     tqdm_class  : [d, tenumerate(), _tmap() (+4 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (12): cpu_count(), _executor_map(), process_map(), Thin wrappers around `concurrent.futures`., Implementation of `thread_map` and `process_map`.      Parameters     ----------, Equivalent of `list(map(fn, *iterables))`     driven by `concurrent.futures.Thre, thread_map(), Tests for `tqdm.contrib.concurrent`. (+4 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (3): dict, MutableMapping, _OrderedDict

### Community 14 - "Community 14"
Cohesion: 0.18
Nodes (12): pos_line_diff(), Test custom bar formatting, Test positioned progress bars, Return differences between two bar output lists.     To be used with `RE_pos`, test_bar_format(), test_float_progress(), test_position(), test_postfix() (+4 more)

### Community 15 - "Community 15"
Cohesion: 0.20
Nodes (7): product(), Thin wrappers around `itertools`., Equivalent of `itertools.product`.      Parameters     ----------     tqdm_class, NoLenIter, Tests for `tqdm.contrib.itertools`., Test contrib.itertools.product, test_product()

### Community 16 - "Community 16"
Cohesion: 0.20
Nodes (5): Force refresh the display of this bar.          Parameters         ----------, Resets to 0 iterations for repeated use.          Consider combining with `leave, Set/modify description of the progress bar.          Parameters         --------, Set/modify description without ': ' appended., Postfix without dictionary expansion, similar to prefix handling.

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (3): Cleanup and (if leave=False) close the progressbar., Use `self.sp` to display `msg` in the specified `pos`.          Consider overloa, Remove from list and reposition other bars         so that newer bars won't over

### Community 19 - "Community 19"
Cohesion: 0.25
Nodes (8): Test clearing bar display, Test refresh bar display, Apply control characters in a string just like a terminal display, squash_ctrlchars(), test_clear(), test_clear_disabled(), test_disabled_refresh(), test_refresh()

### Community 20 - "Community 20"
Cohesion: 0.32
Nodes (4): Clear current bar display., Print a message via tqdm (without overlap with bars)., Disable tqdm within context and refresh tqdm when exits.         Useful when wri, _term_move_up()

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (6): Test external write mode, Test wrapping file-like objects, test_all_defaults(), test_external_write(), test_min_iters(), test_wrapattr()

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (6): Exception, DeprecationError, Test nested progress bars, Test internal GUI properties, test_deprecated_gui(), test_deprecated_nested()

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (3): Backward-compatibility to use: for x in tqdm(iterable), Manually update the progress bar, useful for streams         such as reading fil, Exponential moving average: smoothing to give progressively lower         weight

### Community 24 - "Community 24"
Cohesion: 0.40
Nodes (3): test_format_num(), Set/modify postfix (additional stats)         with automatic formatting based on, Intelligent scientific notation (.3g).          Parameters         ----------

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tqdm` connect `Community 10` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 7`, `Community 8`, `Community 9`, `Community 14`, `Community 16`, `Community 17`, `Community 19`, `Community 20`, `Community 21`, `Community 22`, `Community 23`, `Community 24`, `Community 25`, `Community 26`?**
  _High betweenness centrality (0.507) - this node is a cross-community bridge._
- **Why does `closing()` connect `Community 2` to `Community 1`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 14`, `Community 15`, `Community 19`, `Community 21`, `Community 22`, `Community 26`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Why does `_OrderedDict` connect `Community 13` to `Community 24`, `Community 0`, `Community 3`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `tqdm` (e.g. with `test_pandas_apply_args_deprecation()` and `test_pandas_deprecation()`) actually correct?**
  _`tqdm` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `closing()` (e.g. with `test_process_map()` and `test_thread_map()`) actually correct?**
  _`closing()` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 67 inferred relationships involving `StringIO` (e.g. with `test_process_map()` and `test_thread_map()`) actually correct?**
  _`StringIO` has 67 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `TMonitor` (e.g. with `test_monitor_thread()` and `Bar`) actually correct?**
  _`TMonitor` has 11 INFERRED edges - model-reasoned connections that need verification._
