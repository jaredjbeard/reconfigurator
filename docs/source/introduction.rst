==============================
Introduction to Reconfigurator
==============================

Reconfigurator simplifies the process of setting up and modifying configuration files. With its CLI, you can easily reference local files without affecting the system path. And, if you need to modify a variable, just use the command line and Reconfigurator will handle the rest. No more searching through files to find that one line.

When it comes to running experiments, Reconfigurator can make your life easier too. Instead of manually creating separate config files for each experiment, let Reconfigurator do the heavy lifting. Its markup, based on JSON, allows you to consolidate all the data into one file. Then, you can compile to generate the specific config files you need. This can save you a lot of time and reduce the chance of errors.

For instance, in reinforcement learning, setting up environments and testing various parameters for the learning algorithm can be a hassle. With Reconfigurator, you can generate the config files you need with ease, just like the creator of the tool did. Say goodbye to manual, time-consuming config file generation and try out Reconfigurator today.

Reconfigurator CLI
##################

As mentioned above, the reconfigurator CLI allows us to interact with the local system. We can set where to reference variables. 
Suppose we have a piece of software we are developing that uses internal configuration for paths. By integrating with the reconfigurator, we can reference the defaults with this configuration.
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

Similarly, we can use the reconfigurator to sample from a set of parameters.
This is useful for evaluating algorithms with Monte Carlo trials or hyperparameter tuning, where we want to test a set of parameters to see which one performs best.
More information can be found in the :doc:`Markup Docs Sampling section <../markup>`.