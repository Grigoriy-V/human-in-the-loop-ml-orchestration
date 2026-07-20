# Multi-repository supervision

An umbrella supervisor may inspect multiple repositories, but each action
names exactly one repository and workdir. Ledgers, Git diffs, mutable evidence,
and decisions never cross repository boundaries. Other repositories are
read-only unless a task explicitly names them as its sole writable target.
