------------------------ MODULE Publication ------------------------
EXTENDS Naturals, Sequences, FiniteSets
CONSTANTS Broken, Publishers
Payloads == 1..15
VARIABLES phase, progress, local, base, remote, remoteGen
vars == <<phase, progress, local, base, remote, remoteGen>>
Init == /\ phase = [p \in Publishers |-> "collect"]
        /\ progress = [p \in Publishers |-> 0]
        /\ local = [p \in Publishers |-> [f \in Payloads |-> 0]]
        /\ base = [p \in Publishers |-> 0]
        /\ remote = [f \in Payloads |-> 0]
        /\ remoteGen = 0
Ready(p) == /\ phase[p] = "collect"
            /\ phase' = [phase EXCEPT ![p] = "copy"]
            /\ base' = [base EXCEPT ![p] = remoteGen]
            /\ local' = [local EXCEPT ![p] = remote]
            /\ UNCHANGED <<progress, remote, remoteGen>>
Copy(p) == /\ phase[p] = "copy" /\ progress[p] < Cardinality(Payloads)
           /\ LET f == progress[p] + 1 IN
              local' = [local EXCEPT ![p][f] = IF Broken /\ f = 6 THEN @ ELSE p]
           /\ progress' = [progress EXCEPT ![p] = @ + 1]
           /\ UNCHANGED <<phase, base, remote, remoteGen>>
Fail(p) == /\ phase[p] \in {"collect", "copy"}
           /\ phase' = [phase EXCEPT ![p] = "failed"]
           /\ UNCHANGED <<progress, local, base, remote, remoteGen>>
Push(p) == /\ phase[p] = "copy" /\ progress[p] = Cardinality(Payloads)
           /\ phase' = [phase EXCEPT ![p] = IF base[p] = remoteGen THEN "published" ELSE "rejected"]
           /\ remote' = IF base[p] = remoteGen THEN local[p] ELSE remote
           /\ remoteGen' = IF base[p] = remoteGen THEN p ELSE remoteGen
           /\ UNCHANGED <<progress, local, base>>
Next == (\E p \in Publishers: Ready(p) \/ Copy(p) \/ Fail(p) \/ Push(p))
Spec == Init /\ [][Next]_vars
StaleRejected == \A p \in Publishers: phase[p] = "rejected" => base[p] # remoteGen
CompleteSnapshot == \A f \in Payloads: remote[f] = remoteGen
=============================================================================
