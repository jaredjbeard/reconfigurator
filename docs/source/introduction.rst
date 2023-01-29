==============================
Introduction to Reconfigurator
==============================

Reconfigurator is a tool for setting up and modifying configuration files. 
This is useful in a variety of cases.

- Suppose we have a set of configuration files for a program and we may want to reference them locally, but do not wish to modify the system path. Use of the reconfigurator command line interface allows us to interact with the local system. What's more we can modify variables from the command line and will replace them without needing to hunt down the file and the line of the variable. 

- Suppose we need to run a set of experiments. It may often be the case we need separate configuration files for each experiment. This can be tedious and time consuming. Using our markup built on existing tools such as json, we can easily compress the data into a single file and then sample from it to generate the configuration files we need. As an example, I often run experiments in reinforcement learning. I need to set up environments (e.g. a gridworld with varying numbers of cells or initial positions of the agent). I also then need to look at how various parameters for the learning algorithm affect the performance of the agent. Setting each of these individually can be annoying. It is also subject to errors. What I ended up doing was writing a script to generate the configuration files I needed. And eventually that led to the reconfigurator!

Reconfigurator CLI
##################

As mentioned above, the reconfigurator CLI allows us to interact with the local system. We can set we want to reference variables. 
Suppose we have a piece of software we are developing that uses default configuration paths. By coding with the reconfigurator, we can reference the default paths with an internal configuration.
Then we can use the reconfigurator CLI to modify these attributes. In my case, I have configuration files for default algorithm parameters and environment scenarios. 
By using the reconfigurator, users of my software can easily set their own configurations without needing to modify the source code. 
Then with a quick command line call, they can use their local workspace instead of the default.

Adding CLI
**********

To add reconfigurator command line interface in Linux, navigate to `/home/<user>/.local/lib/python<version#>/site-packages/reconfigurator/reconfigurator/scripts/`.
Then run `sh add_cli.sh`. This will add the reconfigurator CLI to your path. (in the future we may seek to add this at install time).

The reconfigurator can be accessed using `reconfigurator <flag> <args>`. Use `man reconfigurator` for more information.

Markup
######

In the case of markup, the key idea is to leverage existing tools, namely json and yaml, which easily map to native python types. 
By doing so, it remains easy to write and read the configuration files, as well as accessible to new users since these are quite common. 
Essentially, we are using these tools to compress the data into a single file.
Using a few flags and instructions, we "compile" our configuration, expanding it to a set of configurations we require.
Here we provide a brief examples, but checkout the :doc:`Markup Docs <../markup>` for more details. 

Example
*******

Let's say I am running a monte carlo trial to see how the performance of a reinforcement learning agent varies with the number of cells in a gridworld.
I have a set of parameters for the agent and the environment. I want to run 10 trials for each number of cells.

So I write dense markdown as::

    {
        "stitch" : [("x_dim", "y_dim")],
        "x_dim" : [10, 20, 30, 40, 50],
        "y_dim" : [15, 25, 35, 45, 55],
        "n_copies" : 10
    }

Then I call `expand_to_list(<dict>)` to get::
    
    [
        {
            "x_dim" : 10,
            "y_dim" : 15,
        },
        {
            "x_dim" : 10,
            "y_dim" : 25,
        },
        ...
        {
            "x_dim" : 10,
            "y_dim" : 55,
        },
        {
            "x_dim" : 20,
            "y_dim" : 15,
        },
        {
            "x_dim" : 20,
            "y_dim" : 25,
        },
        ...
        {
            "x_dim" : 50,
            "y_dim" : 55,
        },
        {
            "x_dim" : 10,
            "y_dim" : 15,
        },
        ....
    ]
    
Then I can use this to generate the configuration files I need. 
While this is a relatively example, you can see how the utility increases with the number of parameters!

Sampling
########

Under Construction

